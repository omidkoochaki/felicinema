from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from felicinema.apps.cinema.models import Cinema, CinemaSession, Seat, Movie, Ticket
from felicinema.apps.cinema.permissions import IsCinemaOwner, HasCinema
from felicinema.apps.cinema.serializers import CinemaCreateSerializer, CinemaListSerializer, SessionsListSerializer, \
    GenerateSeatsSerializer, MovieCreateSerializer, SessionCreateSerializer


class CreateCinemaView(CreateAPIView):

    serializer_class = CinemaCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({'user_id': request.user.id})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateMovieView(CreateAPIView):
    permission_classes = (HasCinema,)
    serializer_class = MovieCreateSerializer


class ListMovieView(ListAPIView):
    serializer_class = MovieCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        if movie_id == 'all':
            query_set = Movie.objects.all()
        else:
            query_set = Movie.objects.filter(id=movie_id)
        return query_set


class RetriveCinemaView(RetrieveAPIView):
    serializer_class = CinemaListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Cinema.objects.all()


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


class CreateSessionsView(CreateAPIView):
    permission_classes = (IsCinemaOwner,)
    serializer_class = SessionCreateSerializer

    def post(self, request, *args, **kwargs):
        cinema_id = kwargs.pop('cinema_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({
            'cinema_id': cinema_id
        })
        instance = serializer.save()
        tickets = []
        for seat in Seat.objects.filter(cinema_id=cinema_id):
            new_ticket = Ticket()
            new_ticket.session = instance
            new_ticket.seat = seat
            tickets.append(new_ticket)
        Ticket.create_bulk_tickets(tickets)
        return Response({'message': 'The Session and Related Tickets are created!',
                         'data': serializer.data}, status=status.HTTP_201_CREATED)


class GenerateSeatsView(APIView):
    permission_classes = (IsCinemaOwner,)

    def post(self, request, cinema_id):
        data = {
            **request.data,
            'cinema_id': cinema_id
        }
        generate_seat_serializer = GenerateSeatsSerializer(data=data)
        if generate_seat_serializer.is_valid():
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

