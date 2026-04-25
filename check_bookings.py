import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Booking, Room
from datetime import date, timedelta

print("=== ROOM AVAILABILITY DEBUG ===")
print(f"Total bookings: {Booking.objects.count()}")
print(f"Total rooms: {Room.objects.count()}")

# Check all booking statuses
print("\n=== BOOKING STATUSES ===")
for status in ['Pending', 'Confirmed', 'Cancelled', 'Completed']:
    count = Booking.objects.filter(status=status).count()
    print(f"{status}: {count}")

# Show all bookings
print("\n=== ALL BOOKINGS ===")
for b in Booking.objects.all():
    print(f"Room {b.room.id}: {b.check_in} to {b.check_out} ({b.status})")

# Test a specific room with future dates
print("\n=== TEST FUTURE DATES ===")
room = Room.objects.first()
if room:
    # Test far future dates
    future_check_in = date.today() + timedelta(days=30)
    future_check_out = date.today() + timedelta(days=32)
    
    print(f"Testing Room {room.id} for {future_check_in} to {future_check_out}")
    
    # Check what bookings conflict
    conflicting = Booking.objects.filter(
        room=room,
        status__in=['Pending', 'Confirmed'],
        check_in__lt=future_check_out,
        check_out__gt=future_check_in
    )
    
    print(f"Conflicting bookings: {conflicting.count()}")
    for conf in conflicting:
        print(f"  CONFLICT: {conf.check_in} to {conf.check_out} ({conf.status})")
    
    # Test the overlap logic manually
    print(f"\nManual overlap check:")
    for b in Booking.objects.filter(room=room, status__in=['Pending', 'Confirmed']):
        overlap = b.check_in < future_check_out and b.check_out > future_check_in
        print(f"  Booking {b.id}: {b.check_in} to {b.check_out} -> Overlap: {overlap}")
