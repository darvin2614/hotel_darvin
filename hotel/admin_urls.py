from django.urls import path
from . import admin_views

app_name = 'admin_panel'

urlpatterns = [
    # Admin Authentication
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    
    # Admin Dashboard
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Hotel Management
    path('hotels/', admin_views.admin_hotels, name='admin_hotels'),
    path('hotels/add/', admin_views.admin_add_hotel, name='admin_add_hotel'),
    path('hotels/<int:hotel_id>/edit/', admin_views.admin_edit_hotel, name='admin_edit_hotel'),
    path('hotels/<int:hotel_id>/delete/', admin_views.admin_delete_hotel, name='admin_delete_hotel'),
    
    # Room Management
    path('rooms/', admin_views.admin_rooms, name='admin_rooms'),
    path('rooms/add/', admin_views.admin_add_room, name='admin_add_room'),
    path('rooms/<int:room_id>/edit/', admin_views.admin_edit_room, name='admin_edit_room'),
    path('rooms/<int:room_id>/delete/', admin_views.admin_delete_room, name='admin_delete_room'),
    
    # Booking Management
    path('bookings/', admin_views.admin_bookings, name='admin_bookings'),
    path('bookings/<int:booking_id>/confirm/', admin_views.admin_confirm_booking, name='admin_confirm_booking'),
    path('bookings/<int:booking_id>/cancel/', admin_views.admin_cancel_booking, name='admin_cancel_booking'),
    path('bookings/<int:booking_id>/pending/', admin_views.admin_pending_booking, name='admin_pending_booking'),
    path('bookings/<int:booking_id>/delete/', admin_views.admin_delete_booking, name='admin_delete_booking'),
    
    # User Management
    path('users/', admin_views.admin_users, name='admin_users'),
    path('users/<int:user_id>/toggle/', admin_views.admin_toggle_user, name='admin_toggle_user'),
    path('users/<int:user_id>/delete/', admin_views.admin_delete_user, name='admin_delete_user'),
]
