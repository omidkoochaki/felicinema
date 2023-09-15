import random

import jdatetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from felicinema.apps.cinema.models import CinemaSession
from felicinema.apps.cinema.tests import create_user, create_cinema, create_movie


class SessionTests(TestCase):

    def prepare_data(self):
        self.user1, self.user2, self.user3 = create_user(3)
        self.cinema1 = create_cinema(self.user1)  # user1 is a cinema owner
        self.cinema2 = create_cinema(self.user2)  # user2 is a cinema owner
        self.movies = create_movie(3)
        self.session1_1 = CinemaSession.objects.create(
            cinema=self.cinema1,
            movie=self.movies[1],
            date=str(jdatetime.datetime.today().date() + jdatetime.timedelta(days=10)),
            time='14:00:00',
            translation=CinemaSession.Translations.PERSIAN_SUBTITLE
        )
        self.session1_2 = CinemaSession.objects.create(
            cinema=self.cinema1,
            movie=self.movies[1],
            date=str(jdatetime.datetime.today().date() - jdatetime.timedelta(days=15)),
            time='14:00:00',
            translation=CinemaSession.Translations.PERSIAN_SUBTITLE
        )
        self.session2_1 = CinemaSession.objects.create(
            cinema=self.cinema2,
            movie=self.movies[1],
            date=str(jdatetime.datetime.today().date() - jdatetime.timedelta(days=10)),
            time='14:00:00',
            translation=CinemaSession.Translations.PERSIAN_SUBTITLE
        )
        self.client = APIClient()

    def test_session_list_only_contains_future_sessions(self):
        self.prepare_data()
        self.client.force_authenticate(user=self.user2)
        resp = self.client.get(f'/api/v1/cinema/{self.cinema1.id}/sessions/', follow=True)
        self.assertEqual(len(resp.json()), 1)
        self.assertTrue(resp.json()[0].get('date') == self.session1_1.date)
        self.assertTrue(resp.json()[0].get('time') == self.session1_1.time)

    def test_do_not_make_unnecessary_queries(self):
        self.prepare_data()

        def call_sessions_list():
            self.client.get(f'/api/v1/cinema/{self.cinema1.id}/sessions/', follow=True)
        self.assertNumQueries(1, call_sessions_list)

