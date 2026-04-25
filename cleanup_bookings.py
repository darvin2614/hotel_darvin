#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Booking

# Clean up any problematic bookings
print("Cleaning up problematic bookings...")

# Delete any bookings with invalid dates (past dates that might block future bookings)
from datetime import date
today = date.today()

# Remove old bookings that might be blocking
old_bookings = Booking.objects.filter(
    check_out__lt=today,  # Check-out before today
    status__in=['Pending', 'Confirmed']  # Still in pending/confirmed status
)

print(f"Found {old_bookings.count()} old bookings to clean up...")
old_bookings.update(status='Completed')

# Show remaining bookings
print(f"\nRemaining bookings by status:")
for status in ['Pending', 'Confirmed', 'Cancelled', 'Completed']:
    count = Booking.objects.filter(status=status).count()
    print(f"{status}: {count}")

print("\nCleanup completed!")
