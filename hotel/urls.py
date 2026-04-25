from django.urls import path
from . import views

urlpatterns = [
    # Home and main pages
    path('', views.home, name='home'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    
    # Booking
    path('booking/<int:room_id>/', views.booking_page, name='booking'),
    path('booking/verify/<int:room_id>/', views.booking_verify, name='booking_verify'),
    path('booking/confirm/<int:room_id>/', views.booking_confirm, name='booking_confirm'),
    path('booking/confirmed/<int:booking_id>/', views.booking_confirmed, name='booking_confirmed'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('login-verification/', views.login_verification, name='login_verification'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]