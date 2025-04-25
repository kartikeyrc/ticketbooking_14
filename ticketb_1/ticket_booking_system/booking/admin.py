from django.contrib import admin
from .models import Venue, Show, Booking

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name', 'address')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'date', 'price', 'available_seats')
    list_filter = ('venue', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'number_of_tickets', 'total_price', 'status', 'booking_time')
    list_filter = ('status', 'booking_time', 'show')
    search_fields = ('user__username', 'show__title')
    date_hierarchy = 'booking_time'
