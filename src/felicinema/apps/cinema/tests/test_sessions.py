import random

import jdatetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from felicinema.apps.cinema.models import CinemaSession
from felicinema.apps.cinema.tests import create_user, create_cinema, create_movie


class SessionTests(TestCase):

    def test_session_list_only_contains_future_sessions(self):
        user1, user2, user3 = create_user(3)
        cinema1 = create_cinema(user1)  # user1 is a cinema owner
        cinema2 = create_cinema(user2)  # user2 is a cinema owner
        movies = create_movie(3)
        session1_1 = CinemaSession.objects.create(
            cinema=cinema1,
            movie=movies[1],
            date=str(jdatetime.datetime.today().date() + jdatetime.timedelta(days=10)),
            time='14:00:00',
            translation=CinemaSession.Translations.PERSIAN_SUBTITLE
        )
        session1_2 = CinemaSession.objects.create(
            cinema=cinema1,
            movie=movies[1],
            date=str(jdatetime.datetime.today().date() - jdatetime.timedelta(days=15)),
            time='14:00:00',
            translation=CinemaSession.Translations.PERSIAN_SUBTITLE
        )
        session2_1 = CinemaSession.objects.create(
            cinema=cinema2,
            movie=movies[1],
            date=str(jdatetime.datetime.today().date() - jdatetime.timedelta(days=10)),
            time='14:00:00',
            translation=CinemaSession.Translations.PERSIAN_SUBTITLE
        )
        client = APIClient()
        client.force_authenticate(user=user2)
        resp = client.get(f'/api/v1/cinema/{cinema1.id}/sessions/', follow=True)
        self.assertEqual(len(resp.json()), 1)
        self.assertTrue(resp.json()[0].get('date') == session1_1.date)
        self.assertTrue(resp.json()[0].get('time') == session1_1.time)
