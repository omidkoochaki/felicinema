from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from felicinema.apps.accounts.models import User
from felicinema.apps.cinema.models import Cinema, CinemaSession, Movie, Seat


class ShowSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = (
            'row', 'seat', 'wheelchair_friendly',
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
            'title', 'genre', 'duration', 'summary',
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
            'title', 'address', 'language', 'duration', 'summary'
        )


class CinemaListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source='user')
    seats = ShowSeatsSerializer(many=True)

    class Meta:
        model = Cinema
        fields = (
            'id', 'title', 'address', 'owner', 'seats'
        )


class SessionsListSerializer(serializers.ModelSerializer):
    movie = MovieCreateSerializer()
    cinema = CinemaListSerializer()
    class Meta:
        model = CinemaSession
        fields = (
            'movie', 'date', 'time', 'translation', 'description', 'cinema', 'tickets'
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
        print(type(style))
        if type(style) is not list:
            raise serializers.ValidationError(err_msg)
        if style == []:
            raise serializers.ValidationError(err_msg)
        return style

    def validate_cinema_id(self, cinema_id):
        cinema = get_object_or_404(Cinema, id=cinema_id)
        return cinema_id

