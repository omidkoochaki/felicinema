from django.urls import path

from felicinema.apps.cinema.views import CreateCinemaView, ListCinemaView, ListSessionsView, GenerateSeatsView, \
    CreateMovieView, ListMovieView, RetriveCinemaView, CreateSessionsView, CreateReservationView, AcceptReservationView

urlpatterns = [
    path('add/', CreateCinemaView.as_view()),
    path('add/<int:cinema_id>/seats/', GenerateSeatsView.as_view()),
    path('all/', ListCinemaView.as_view()),
    path('<int:pk>/', RetriveCinemaView.as_view()),
    path('movie/add/', CreateMovieView.as_view()),
    path('movie/<movie_id>/', ListMovieView.as_view()),
    path('<int:cinema_id>/sessions/', ListSessionsView.as_view()),
    path('<int:cinema_id>/sessions/<int:session_id>/reserve/', CreateReservationView.as_view()),
    path('<int:cinema_id>/sessions/add/', CreateSessionsView.as_view()),
    path('reservation/<uuid:pid>/', AcceptReservationView.as_view(),)  # send is_paid = True/false for accept/reject
]
