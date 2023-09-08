import datetime
import jdatetime
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from django.db import models

from felicinema.apps.accounts.validators import phone_validator


class CustomUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return super().create_superuser(username=username, email=email, password=password, birth_year=1989)


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'

    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)
    _birth_year = models.PositiveIntegerField(validators=[MinValueValidator(1300)], db_column='birth_year')
    description = models.TextField(blank=True)

    objects = CustomUserManager()

    @property
    def birth_year(self):
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value):
        self._birth_year = value

    @property
    def age(self):
        if int(self.birth_year) > 1900:
            year = datetime.datetime.today().year
        else:
            year = jdatetime.datetime.today().year
        return year - int(self.birth_year)

    @property
    def is_cinema_owner(self):
        return hasattr(self, 'cinema')

    def __str__(self):
        return self.first_name + self.last_name
