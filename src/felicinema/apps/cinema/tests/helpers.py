import random

from felicinema.apps.accounts.models import User
from felicinema.apps.cinema.models import Cinema, Movie


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


def create_cinema(user: User):
    return Cinema.objects.create(
        user=user,
        title=f'cinema for {user.username}',
        address=f'address for {user.username}'
    )


def create_user(number=1):
    users = []
    for i in range(number):
        users.append(User.objects.create_user(
            username=f'test-user-{i}',
            password='pass',
            email=f'user{i}@test.com',
            birth_year=1368
        ))
    return users
