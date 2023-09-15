import random

from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APIClient

from felicinema.apps.accounts.models import User
from felicinema.apps.cinema.models import Cinema, Movie


class MovieTests(TestCase):

    @staticmethod
    def create_movie(number=1, genre='fiction'):
        movies = []
        for i in range(number):
            movies.append(Movie.objects.create(
                title=f"movie {i} title",
                genre=genre,
                duration=f'2:{random.randint(10, 59)}:{random.randint(10, 59)}',
                summary=f'summary for movie {i}',
                language=random.choice(Movie.Language.choices)[0]
            ))
        return movies

    @staticmethod
    def create_cinema(user: User):
        return Cinema.objects.create(
            user=user,
            title=f'cinema for {user.username}',
            address=f'address for {user.username}'
        )

    @staticmethod
    def create_user(number=1):
        users = []
        for i in range(number):
            users.append(User.objects.create_user(
                username=f'test-user-{i + 300}',
                password='pass',
                email=f'user{i}@test.com',
                birth_year=1368
            ))
        return users

    def test_authorized_users_can_see_movies_list(self):
        client = APIClient()
        user = self.create_user()[0]
        movies = self.create_movie(5)
        resp = client.get('/api/v1/cinema/movie/all/', follow=True)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        client.force_authenticate(user=user)
        resp = client.get('/api/v1/cinema/movie/all/', follow=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 5)

    def test_only_cinema_owners_can_add_movies(self):

        client = APIClient()
        user1, user2 = self.create_user(2)
        cinema = self.create_cinema(user1)  # user1 is a cinema owner

        client.force_authenticate(user=user2)
        movie_data = {
            'title': 'some_title',
            'genre': 'some_genre',
            'duration': '2:35:17',
            'summary': 'summary for some_title movie',
            'language': 'O'
        }
        response = client.post('/api/v1/cinema/movie/add/', movie_data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.force_authenticate(user=user1)
        response = client.post('/api/v1/cinema/movie/add/', movie_data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
