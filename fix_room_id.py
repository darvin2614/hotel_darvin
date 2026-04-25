#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Hotel, Room

def create_room_id_1():
    """Create a room with ID 1 to fix 404 error"""
    
    # Get first hotel or create one
    hotel = Hotel.objects.first()
    if not hotel:
        print("No hotels found. Creating a default hotel...")
        hotel = Hotel.objects.create(
            name="Grand Palace Hotel",
            city="Mumbai",
            address="123 Palace Road, Mumbai",
            rating=4.5,
            hotel_image_url="https://via.placeholder.com/800x600"
        )
        print(f"Created hotel: {hotel.name}")
    
    # Check if room with ID 1 already exists
    if Room.objects.filter(id=1).exists():
        print("Room with ID 1 already exists!")
        room = Room.objects.get(id=1)
        print(f"Room ID 1: {room.get_room_type_display()} at {hotel.name}")
        return
    
    # Create room with ID 1
    room = Room.objects.create(
        id=1,  # Force ID 1
        hotel=hotel,
        room_type='DELUXE',
        room_number='101',
        price_per_night=5000,
        capacity=2,
        availability=True,
        room_image_url="https://via.placeholder.com/600x400"
    )
    
    print(f"✅ Created Room ID 1: {room.get_room_type_display()} Room {room.room_number}")
    print(f"   Hotel: {hotel.name}")
    print(f"   Price: ₹{room.price_per_night}/night")
    print(f"   Capacity: {room.capacity} guests")
    print("🎉 Room ID 1 is now available at /rooms/1/")

if __name__ == "__main__":
    create_room_id_1()
