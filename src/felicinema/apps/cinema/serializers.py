from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from felicinema.apps.accounts.models import User
from felicinema.apps.cinema.models import Cinema, CinemaSession, Movie, Seat, Ticket, Payment


class ShowSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = (
            'id', 'row', 'seat', 'wheelchair_friendly',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name'
        )


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'title', 'genre', 'duration', 'summary', 'language',
        )

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)

    def validate_duration(self, dur):
        err_msg = 'duration must be a str like: "02:30:00" for a duration of 2 hours and a half.'
        if len(str(dur)) != 7:
            raise serializers.ValidationError(err_msg)
        return dur


class CinemaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = (
            'title', 'address',
        )


class CinemaListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source='user')
    seats = ShowSeatsSerializer(many=True)

    class Meta:
        model = Cinema
        fields = (
            'id', 'title', 'address', 'owner', 'seats'
        )


class CinemaListForSessionSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source='user')

    class Meta:
        model = Cinema
        fields = (
            'id', 'title', 'address', 'owner',
        )


class TicketReserveSerializer(serializers.Serializer):
    seat_id = serializers.IntegerField(min_value=0)
    cinema_id = serializers.IntegerField(min_value=0)
    session_id = serializers.IntegerField(min_value=0)


class TicketSerializer(serializers.ModelSerializer):
    seat = ShowSeatsSerializer()

    class Meta:
        model = Ticket
        fields = ('session', 'seat', 'state')


class PaymentDetailSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()

    class Meta:
        model = Payment
        fields = ('ticket', 'is_paid')


class PaymentAcceptSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=0)
    is_paid = serializers.BooleanField(required=True)

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)

    def validate_code(self, code):
        if int(code) == int(self.instance.code):
            return code
        raise serializers.ValidationError("code is not acceptable")

    def validate_is_paid(self, is_paid):
        if type(is_paid) == bool:
            return is_paid
        raise serializers.ValidationError("is_paid")

    def update(self, instance, validated_data):
        instance.is_paid = validated_data.get('is_paid')
        instance.save()
        return instance


class SessionsListSerializer(serializers.ModelSerializer):
    movie = MovieCreateSerializer()
    cinema = CinemaListForSessionSerializer()
    tickets = TicketSerializer(many=True)

    class Meta:
        model = CinemaSession
        fields = (
            'id', 'movie', 'date', 'time', 'translation', 'description', 'cinema', 'tickets'
        )


class SessionCreateSerializer(serializers.ModelSerializer):
    # todo: add validators for time and date to prevent adding session in the past
    class Meta:
        model = CinemaSession
        fields = (
            'movie', 'date', 'time', 'translation', 'description'
        )


class GenerateSeatsSerializer(serializers.Serializer):
    cinema_id = serializers.IntegerField(min_value=0)
    style = serializers.JSONField()

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)

    def validate_style(self, style):
        err_msg = "style should be like this: [[0,0,0,0], [0,0,0]]"
        if type(style) is not list:
            raise serializers.ValidationError(err_msg)
        if style == []:
            raise serializers.ValidationError(err_msg)
        return style

    def validate_cinema_id(self, cinema_id):
        cinema = get_object_or_404(Cinema, id=cinema_id)
        return cinema_id
