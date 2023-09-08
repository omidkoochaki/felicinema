from django.urls import path

from felicinema.apps.cinema.views import CreateCinemaView, ListCinemaView, ListSessionsView, GenerateSeatsView, \
    CreateMovieView, ListMovieView, RetriveCinemaView

urlpatterns = [
    path('add/', CreateCinemaView.as_view()),
    path('add/<int:cinema_id>/seats/', GenerateSeatsView.as_view()),
    path('movie/add/', CreateMovieView.as_view()),
    path('movie/<movie_id>/', ListMovieView.as_view()),
    path('all/', ListCinemaView.as_view()),
    path('<int:pk>/', RetriveCinemaView.as_view()),
    path('<int:cinema_id>/sessions/', ListSessionsView.as_view()),
]
