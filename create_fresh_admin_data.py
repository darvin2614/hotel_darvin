import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from django.contrib.auth.models import User
from hotel.models import Hotel, Room, Booking
from datetime import date, timedelta
import random

print("Creating fresh admin panel dummy data...")

# Create admin user
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@hotel.com',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.first_name = 'Admin'
    admin_user.save()
    print('✓ Created admin user: admin@hotel.com / admin123')
else:
    print('✓ Admin user already exists')

# Create dummy hotels
hotels_data = [
    {
        'name': 'Taj Coromandel Chennai',
        'city': 'Chennai',
        'address': '35, Mahatma Gandhi Road, Chennai',
        'description': 'Luxury hotel with contemporary design and traditional South Indian hospitality.',
        'rating': 4.5,
        'price_range': '$$$$',
        'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    },
    {
        'name': 'ITC Grand Chola Chennai',
        'city': 'Chennai',
        'address': '63, Mount Road, Chennai',
        'description': 'Magnificent luxury hotel inspired by Dravidian architecture.',
        'rating': 4.6,
        'price_range': '$$$$',
        'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    },
    {
        'name': 'Taj Mahal Palace Mumbai',
        'city': 'Mumbai',
        'address': 'Apollo Bandar, Colaba, Mumbai',
        'description': 'Iconic luxury hotel offering stunning views of the Arabian Sea.',
        'rating': 4.8,
        'price_range': '$$$$',
        'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    },
    {
        'name': 'The Leela Palace Bangalore',
        'city': 'Bangalore',
        'address': '23, Old Airport Road, Bangalore',
        'description': 'Royal charm combined with modern amenities.',
        'rating': 4.7,
        'price_range': '$$$$',
        'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    },
    {
        'name': 'The Leela Palace New Delhi',
        'city': 'Delhi',
        'address': 'Chanakyapuri, New Delhi',
        'description': 'Luxurious accommodation in the diplomatic enclave.',
        'rating': 4.7,
        'price_range': '$$$$',
        'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    },
]

created_hotels = []
for hotel_data in hotels_data:
    hotel, created = Hotel.objects.get_or_create(
        name=hotel_data['name'],
        defaults=hotel_data
    )
    if created:
        created_hotels.append(hotel)
        print(f'✓ Created hotel: {hotel.name}')

# Create rooms for each hotel
room_types = ['Single', 'Double', 'Deluxe', 'Suite']
room_images = [
    'https://images.unsplash.com/photo-1611892440504-42a792e24a34?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1596394519210-1b6a7e03d6f9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1584132967334-56e969fb9fc5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
]

for hotel in Hotel.objects.all():
    for i, room_type in enumerate(room_types):
        room_number = f"{hotel.name[0]}{i+1:02d}"
        base_prices = {'Single': 50, 'Double': 80, 'Deluxe': 120, 'Suite': 200}
        city_multiplier = {'Chennai': 1.0, 'Mumbai': 1.3, 'Bangalore': 1.2, 'Delhi': 1.1}
        
        price = base_prices[room_type] * city_multiplier.get(hotel.city, 1.0)
        price = round(price, -1)  # Round to nearest 10
        
        room, created = Room.objects.get_or_create(
            hotel=hotel,
            room_number=room_number,
            defaults={
                'room_type': room_type,
                'price_per_night': price,
                'capacity': {'Single': 1, 'Double': 2, 'Deluxe': 2, 'Suite': 4}[room_type],
                'availability': True,
                'description': f"Spacious {room_type.lower()} room at {hotel.name}.",
                'room_image_url': room_images[i]
            }
        )
        if created:
            print(f'  ✓ Created room: {room.room_number} - {room_type}')

# Create dummy users
users_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    {'username': 'sarah_jones', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Jones'},
    {'username': 'david_brown', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown'},
]

created_users = []
for user_data in users_data:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'username': user_data['username'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name']
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        created_users.append(user)
        print(f'✓ Created user: {user.email}')

# Create dummy bookings
all_users = list(User.objects.filter(is_superuser=False))
all_rooms = list(Room.objects.all())
statuses = ['Pending', 'Confirmed', 'Cancelled']

created_bookings = []
for i in range(12):  # Create 12 dummy bookings
    if all_users and all_rooms:
        user = random.choice(all_users)
        room = random.choice(all_rooms)
        status = random.choice(statuses)
        
        # Random dates within next 30 days
        check_in = date.today() + timedelta(days=random.randint(1, 25))
        check_out = check_in + timedelta(days=random.randint(1, 4))
        
        booking, created = Booking.objects.get_or_create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            defaults={
                'hotel': room.hotel,
                'total_amount': (check_out - check_in).days * room.price_per_night,
                'status': status
            }
        )
        if created:
            created_bookings.append(booking)
            print(f'✓ Created booking: #{booking.id} - {status}')

# Summary
print('\n📊 FRESH ADMIN DATA SUMMARY:')
print(f'   Admin User: {User.objects.filter(is_superuser=True).count()}')
print(f'   Regular Users: {User.objects.filter(is_superuser=False).count()}')
print(f'   Hotels: {Hotel.objects.count()}')
print(f'   Rooms: {Room.objects.count()}')
print(f'   Bookings: {Booking.objects.count()}')
print(f'   Pending: {Booking.objects.filter(status="Pending").count()}')
print(f'   Confirmed: {Booking.objects.filter(status="Confirmed").count()}')
print(f'   Cancelled: {Booking.objects.filter(status="Cancelled").count()}')
print('\n🔑 Admin login: admin@hotel.com / admin123')
print('\n✅ Fresh admin panel data ready!')
