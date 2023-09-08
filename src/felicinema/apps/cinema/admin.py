from django.contrib import admin

from felicinema.apps.cinema.models import Seat, Cinema, Movie

admin.site.register(Cinema)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['cinema', 'row', 'seat', 'wheelchair_friendly']


@admin.register(Movie)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'duration', 'summary']
