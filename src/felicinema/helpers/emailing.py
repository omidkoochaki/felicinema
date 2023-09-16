from django.conf import settings
from django.core.mail import send_mail
from felicinema.celery import app as celery_app


@celery_app.task(bind=True, name="send_reserve_request_info")
def send_reserve_request_info(self, cinema_owner, date, time, movie, reservant, code, payment_id, cinema_owner_email):
    subject = 'Reservation Request from Felicinema'
    message = f'Hi {cinema_owner},\n' \
              f' you have a reservation request for: \n' \
              f'date: {date} \n' \
              f'time: {time} \n' \
              f'movie: {movie} \n' \
              f'from: {reservant} \n' \
              f'the security code for this reservation is: {code}\n' \
              f'\n' \
              f'To accept the reservation please go to the link below and enter the security code: \n' \
              f'cinema/reservation/{payment_id}/ \n' \
              f'Or you can check your dashboard and accept the requests you want. \n' \
              f'Regards, \n' \
              f'Omid from FeliCinema'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [cinema_owner_email, ]
    send_mail(subject, message, email_from, recipient_list)


@celery_app.task(bind=True, name="send_reservation_result_to_reservant")
def send_reservation_result_to_reservant(self, reservant, date, time, movie, cinema_owner, reservant_email, accepted):
    subject = 'Reservation Result Report from Felicinema'
    print('=============================> 1')
    message = f"Hello {reservant} \n" \
              f"Your reservation request for:\n" \
              f'date: {date} \n' \
              f'time: {time} \n' \
              f'movie: {movie} \n' \
              f'has been {"Accepted" if accepted else "Rejected"} by: {cinema_owner} \n' \
              f'{"Enjoy the event!" if accepted else "Try other events!"}' \
              f'\n' \
              f'Regards, \n' \
              f'Omid from FeliCinema'
    print('=============================> 2')
    print(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [reservant_email, ]
    send_mail(subject, message, email_from, recipient_list)


