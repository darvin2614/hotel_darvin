#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Booking, Room
from datetime import date, timedelta

print("=== BOOKING AVAILABILITY DEBUG ===")
print(f"Total bookings: {Booking.objects.count()}")
print(f"Total rooms: {Room.objects.count()}")

print("\n=== BOOKING STATUSES ===")
for status in ['Pending', 'Confirmed', 'Cancelled', 'Completed']:
    count = Booking.objects.filter(status=status).count()
    print(f"{status}: {count}")

print("\n=== SAMPLE BOOKINGS ===")
for b in Booking.objects.all()[:10]:
    print(f"Room {b.room.id}: {b.check_in} to {b.check_out} ({b.status})")

print("\n=== TEST AVAILABILITY FOR ROOM 1 ===")
room = Room.objects.first()
if room:
    # Test future dates
    future_check_in = date.today() + timedelta(days=10)
    future_check_out = date.today() + timedelta(days=12)
    
    print(f"Testing Room {room.id} for {future_check_in} to {future_check_out}")
    
    # Check the actual query
    conflicting = Booking.objects.filter(
        room=room,
        status__in=['Pending', 'Confirmed'],
        check_in__lt=future_check_out,
        check_out__gt=future_check_in
    )
    
    print(f"Conflicting bookings found: {conflicting.count()}")
    for conf in conflicting:
        print(f"  - {conf.check_in} to {conf.check_out} ({conf.status})")
    
    print(f"Room available: {not conflicting.exists()}")

print("\n=== CHECK ALL ROOMS FOR FUTURE DATES ===")
future_check_in = date.today() + timedelta(days=10)
future_check_out = date.today() + timedelta(days=12)

for room in Room.objects.all()[:5]:
    conflicting = Booking.objects.filter(
        room=room,
        status__in=['Pending', 'Confirmed'],
        check_in__lt=future_check_out,
        check_out__gt=future_check_in
    )
    print(f"Room {room.id}: Available = {not conflicting.exists()} (Conflicts: {conflicting.count()})")
