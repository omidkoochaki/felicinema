from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from felicinema.apps.cinema.models import Cinema, CinemaSession, Seat
from felicinema.apps.cinema.permissions import IsCinemaOwner
from felicinema.apps.cinema.serializers import CinemaCreateSerializer, CinemaListSerializer, SessionsListSerializer, \
    GenerateSeatsSerializer, MovieCreateSerializer


class CreateCinemaView(CreateAPIView):

    serializer_class = CinemaCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            'user_id': request.user.id
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        print('=+' * 30)
        serializer.validated_data.update({'user_id': request.user.id})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateMovieView(CreateAPIView):
    permission_classes = (IsCinemaOwner,)
    serializer_class = MovieCreateSerializer


class ListCinemaView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CinemaListSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        title = query_params.get('title')
        address = query_params.get('address')
        if title or address:
            queryset = Cinema.objects.search_title_and_address(title, address)
        else:
            queryset = Cinema.objects.all()
        return queryset


class ListSessionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionsListSerializer

    def get_queryset(self):
        cinema_id = self.kwargs['cinema_id']
        query_set = CinemaSession.objects.get_cinema_future_sessions(cinema_id)
        return query_set


class GenerateSeatsView(APIView):
    permission_classes = (IsCinemaOwner,)

    def post(self, request, cinema_id):
        data = {
            **request.data,
            'cinema_id': cinema_id
        }
        generate_seat_serializer = GenerateSeatsSerializer(data=data)
        # print('1 ===========> ', generate_seat_serializer.validated_data)
        if generate_seat_serializer.is_valid():
            print('2 ===========> ', generate_seat_serializer.validated_data)
            style = generate_seat_serializer.validated_data.get('style')
            cinema_id = generate_seat_serializer.validated_data.get('cinema_id')
            for i, row in enumerate(style):
                for j, seat in enumerate(row):
                    new_seat = Seat()
                    new_seat.cinema_id = cinema_id
                    new_seat.row = i+1
                    new_seat.seat = j+1
                    new_seat.wheelchair_friendly = False if seat == 0 else True
                    new_seat.save()
            return Response(data={'message': 'all seats are created!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

