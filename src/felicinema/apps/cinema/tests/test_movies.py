from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


from felicinema.apps.cinema.tests.helpers import create_user, create_movie, create_cinema


class MovieTests(TestCase):

    def test_authorized_users_can_see_movies_list(self):
        client = APIClient()
        user = create_user()[0]
        movies = create_movie(5)
        resp = client.get('/api/v1/cinema/movie/all/', follow=True)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        client.force_authenticate(user=user)
        resp = client.get('/api/v1/cinema/movie/all/', follow=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 5)

    def test_only_cinema_owners_can_add_movies(self):

        client = APIClient()
        user1, user2 = create_user(2)
        cinema = create_cinema(user1)  # user1 is a cinema owner

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
