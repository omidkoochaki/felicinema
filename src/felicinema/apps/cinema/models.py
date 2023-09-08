import random

import jdatetime
from django.db import models
from django.db.models import Q

from felicinema.apps.accounts.models import User


class CinemaManager(models.Manager):
    def search_title_and_address(self, title=None, address=None):
        q = Q(title__contains=title) | Q(address__contains=title) | \
            Q(title__contains=address) | Q(address__contains=address)
        return self.filter(q)


class Cinema(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    address = models.TextField()  # TODO: handle this with a one to one field from address models

    objects = CinemaManager()

    def __str__(self):
        return self.title


class Movie(models.Model):
    class Language(models.TextChoices):
        PERSIAN = 'P', 'Persian'
        ENGLISH = 'E', 'English'
        OTHER = 'O', 'Other'

    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=128)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.ENGLISH)
    duration = models.DurationField()
    summary = models.TextField()
    # todo: add poster


class SessionManager(models.Manager):
    def get_movies(self, movie_name: str = None, address: str = None):
        return self.filter(movie_title__contains=movie_name, cinema_address__contains=address)

    def get_cinema_future_sessions(self, cinema_id):
        q = Q(cinema_id=cinema_id) & Q(date__gte=jdatetime.datetime.now().date().isoformat()) & \
            Q(time__gte=jdatetime.datetime.now().time().isoformat())
        return self.filter(q)


class CinemaSession(models.Model):
    class Translations(models.TextChoices):
        PERSIAN_SUBTITLE = 'PS', 'Persian Subtitle'
        ENGLISH_SUBTITLE = 'ES', 'English Subtitle'
        OTHER_SUBTITLE = 'OS', 'Other Subtitle'
        PERSIAN_VOICE = 'PV', 'Persian Voice'
        ENGLISH_VOICE = 'EV', 'English Voice'
        OTHER_VOICE = 'OV', 'Other Voice'
    cinema = models.OneToOneField(Cinema, on_delete=models.CASCADE, related_name='sessions')
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    time = models.TimeField()
    translation = models.CharField(max_length=2, choices=Translations.choices, default=Translations.PERSIAN_SUBTITLE)
    description = models.TextField(null=True, blank=True)

    objects = SessionManager()


class Seat(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    wheelchair_friendly = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seat', 'row', 'cinema')


class Ticket(models.Model):
    class RESERVATION(models.TextChoices):
        OCCUPIED = 'O', 'Occupied'
        RESERVING = 'R', 'Reserving'
        FREE = 'F', 'FREE'

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # the user who wants to see movie
    session = models.ForeignKey(CinemaSession, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    state = models.CharField(max_length=1, choices=RESERVATION.choices, default=RESERVATION.FREE)

    class Meta:
        unique_together = ('seat', 'session',)

    @property
    def is_free(self):
        if self.state == self.RESERVATION.FREE:
            return True
        return False

    @property
    def is_reserving(self):
        if self.state == self.RESERVATION.RESERVING:
            return True
        return False

    @property
    def is_occupied(self):
        if self.state == self.RESERVATION.OCCUPIED:
            return True
        return False

    def reserve(self, seat: Seat, user: User) -> str:
        if self.is_free:
            self.state = Ticket.RESERVATION.RESERVING
            self.seat = seat
            self.user = user
            ticket = self.save()
            payment = Payment()
            payment.make_payment(ticket)
            return self.state
        elif self.is_reserving:
            if self.user == user and self.seat == seat:
                if hasattr(self, 'payment'):
                    if self.payment.is_paid:
                        self.state = Ticket.RESERVATION.OCCUPIED
                        self.save()
                        return self.state
                    else:
                        raise Exception("Payment is not done.")
                raise Exception("No Payment Found --- Probably Facing a BUG")
            raise Exception("Seat is probably reserving by another user")
        elif self.is_occupied:
            raise Exception("Seat is reserved before")
        else:
            raise Exception("maybe a BUG")


class Payment(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    is_paid = models.BooleanField(default=False)

    def send_email_to_user(self):
        pass

    def send_email_to_cinema_owner(self):
        owner = self.ticket.session.cinema.user
        code = self.code
        user = self.ticket.user
        # create a celery task and call it here to send email
        pass

    def make_payment(self, ticket):
        self.ticket = ticket
        self.code = random.randint(100000, 999999)
        self.is_paid = False
        self.save()
        self.send_email_to_cinema_owner()

    def check_payment(self, code):
        if self.code == code:
            self.is_paid = True
            self.save()
            return True
        return False