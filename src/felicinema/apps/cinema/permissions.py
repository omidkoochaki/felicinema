from rest_framework.permissions import IsAuthenticated

from felicinema.apps.cinema.models import Cinema


class IsCinemaOwner(IsAuthenticated):
    # TODO: try this with object perms
    def has_permission(self, request, view):
        cinema_id = view.kwargs.get('cinema_id')
        if Cinema.objects.filter(id=cinema_id).exists():
            if request.user.is_cinema_owner and request.user.cinema == Cinema.objects.get(id=cinema_id):
                return super().has_permission(request, view)
        return False


class HasCinema(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_cinema_owner
