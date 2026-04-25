from django.contrib import admin
from .models import Hotel, Room, Booking


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'rating', 'price_range', 'created_at']
    list_filter = ['city', 'rating', 'price_range']
    search_fields = ['name', 'city', 'address']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hotel', 'room_type', 'price_per_night', 'capacity', 'availability']
    list_filter = ['room_type', 'availability', 'hotel__city']
    search_fields = ['room_number', 'hotel__name', 'room_type']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['hotel', 'room_number']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('hotel')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'room', 'check_in', 'check_out', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'hotel__city']
    search_fields = ['user__username', 'hotel__name', 'room__room_number']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'hotel', 'room')
    
    actions = ['confirm_booking', 'cancel_booking']
    
    def confirm_booking(self, request, queryset):
        queryset.update(status='Confirmed')
    confirm_booking.short_description = "Mark selected bookings as confirmed"
    
    def cancel_booking(self, request, queryset):
        queryset.update(status='Cancelled')
    cancel_booking.short_description = "Mark selected bookings as cancelled"