#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Room, Booking
from datetime import date, timedelta

def test_room_availability():
    """Test room availability logic"""
    
    # Get Room 1
    room = Room.objects.get(id=1)
    print(f"Testing Room {room.id}: {room.get_room_type_display()} at {room.hotel.name}")
    
    # Test dates (tomorrow to day after tomorrow)
    today = date.today()
    check_in = today + timedelta(days=1)
    check_out = today + timedelta(days=2)
    
    print(f"Testing dates: {check_in} to {check_out}")
    
    # Check existing bookings
    existing_bookings = Booking.objects.filter(
        room=room,
        status__in=['Pending', 'Confirmed']
    )
    
    print(f"Existing bookings for Room 1: {existing_bookings.count()}")
    for booking in existing_bookings:
        print(f"  - {booking.check_in} to {booking.check_out} ({booking.status})")
    
    # Test availability logic (same as in views.py)
    conflicting_bookings = Booking.objects.filter(
        room=room,
        status__in=['Pending', 'Confirmed'],
        check_in__lt=check_out,  # existing check-in before new check-out
        check_out__gt=check_in   # existing check-out after new check-in
    )
    
    print(f"Conflicting bookings: {conflicting_bookings.count()}")
    for booking in conflicting_bookings:
        print(f"  CONFLICT: {booking.check_in} to {booking.check_out} ({booking.status})")
    
    # Check if room is available
    is_available = not conflicting_bookings.exists()
    print(f"Room available: {is_available}")
    
    if is_available:
        print("✅ Room should be available for booking!")
    else:
        print("❌ Room is NOT available for booking!")

if __name__ == "__main__":
    test_room_availability()
