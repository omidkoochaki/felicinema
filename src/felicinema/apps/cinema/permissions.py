from rest_framework.permissions import IsAuthenticated

from felicinema.apps.cinema.models import Cinema


class IsCinemaOwner(IsAuthenticated):
    # TODO: try this with object perms
    def has_permission(self, request, view):
        cinema_id = view.kwargs.get('cinema_id')
        if Cinema.objects.filter(id=cinema_id).exists():  # todo: replace with try/except
            if request.user.has_cinema and request.user.cinema == Cinema.objects.get(id=cinema_id):
                return super().has_permission(request, view)
        return False


class HasCinema(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.has_cinema


class CinemaHasNotSeats(IsCinemaOwner):
    # TODO: try this with object perms
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            cinema_id = view.kwargs.get('cinema_id')
            try:
                cinema = Cinema.objects.get(id=cinema_id)
                if cinema.has_seats:
                    return False
                return True
            except Exception as e:
                print(e)
                return False
