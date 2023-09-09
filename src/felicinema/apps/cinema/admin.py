from django.contrib import admin

from felicinema.apps.cinema.models import Seat, Cinema, Movie, Ticket, CinemaSession, Payment

admin.site.register(Cinema)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['cinema', 'row', 'seat', 'wheelchair_friendly']


@admin.register(Movie)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'duration', 'summary']


@admin.register(Ticket)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['session', 'seat', 'state']
    list_editable = ['state']


@admin.register(CinemaSession)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['cinema', 'movie', 'date', 'time']


@admin.register(Payment)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'code', 'is_paid']
