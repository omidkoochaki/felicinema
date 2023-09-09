from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from felicinema.apps.cinema.models import Cinema, CinemaSession, Seat, Movie, Ticket, Payment
from felicinema.apps.cinema.permissions import IsCinemaOwner, HasCinema
from felicinema.apps.cinema.serializers import CinemaCreateSerializer, CinemaListSerializer, SessionsListSerializer, \
    GenerateSeatsSerializer, MovieCreateSerializer, SessionCreateSerializer, TicketReserveSerializer, \
    PaymentAcceptSerializer, PaymentDetailSerializer


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
        try:
            instance = serializer.save()
        except Exception as e:
            return Response({'messsage': str(e)}, status=status.HTTP_403_FORBIDDEN)
        tickets = []
        for seat in Seat.objects.filter(cinema_id=cinema_id):
            new_ticket = Ticket()
            new_ticket.session = instance
            new_ticket.seat = seat
            tickets.append(new_ticket)
        Ticket.create_bulk_tickets(tickets)
        return Response({'message': 'The Session and Related Tickets are created!',
                         'data': serializer.data}, status=status.HTTP_201_CREATED)


class CreateReservationView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        cinema_id = kwargs.pop('cinema_id')
        session_id = kwargs.pop('session_id')
        data = {
            **request.data,
            'cinema_id': cinema_id,
            'session_id': session_id,
        }
        serializer = TicketReserveSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                ticket = Ticket.objects.get(
                    session_id=serializer.validated_data.get('session_id'),
                    seat_id=serializer.validated_data.get('seat_id')
                )
                ticket.reserve(seat_id=serializer.validated_data.get('seat_id'), user=request.user)
                return Response(
                    {'messsage': 'reservation is started, we will send you an email if host accepts your reservation'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({'messsage': str(e)}, status=status.HTTP_403_FORBIDDEN)


class AcceptReservationView(APIView):
    permission_classes = (HasCinema,)

    def get(self, request, pid):
        payment = get_object_or_404(Payment, id=pid)
        car_serializer = PaymentDetailSerializer(instance=payment)
        data = car_serializer.data
        return Response({'payment': data})

    def put(self, request, pid):
        payment = get_object_or_404(Payment, id=pid)
        payment_serializer = PaymentAcceptSerializer(
            instance=payment,
            data=request.data,
            partial=True
        )

        if payment_serializer.is_valid():
            payment_serializer.save()
            # todo: add a signal here to update Ticket state to FREE or OCCUPIED
            return Response({'message': 'Reservation Updated successfully!'})

        return Response({'message': payment_serializer.errors})


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

