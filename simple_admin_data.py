from django.contrib.auth.models import User
from hotel.models import Hotel, Room, Booking
from datetime import date, timedelta
import random

# Create admin user
if not User.objects.filter(email='admin@hotel.com').exists():
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@hotel.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    print('✓ Created admin user: admin@hotel.com / admin123')
else:
    print('✓ Admin user already exists')

# Create some dummy hotels if none exist
if Hotel.objects.count() == 0:
    hotels_data = [
        {
            'name': 'Taj Coromandel Chennai',
            'city': 'Chennai',
            'address': '35, Mahatma Gandhi Road, Chennai',
            'description': 'Luxury hotel with contemporary design.',
            'rating': 4.5,
            'price_range': '$$$$',
            'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Taj Mahal Palace Mumbai',
            'city': 'Mumbai',
            'address': 'Apollo Bandar, Colaba, Mumbai',
            'description': 'Iconic luxury hotel.',
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
    ]
    
    for hotel_data in hotels_data:
        hotel = Hotel.objects.create(**hotel_data)
        print(f'✓ Created hotel: {hotel.name}')
        
        # Create rooms for each hotel
        room_types = ['Single', 'Double', 'Deluxe']
        for i, room_type in enumerate(room_types):
            room = Room.objects.create(
                hotel=hotel,
                room_type=room_type,
                room_number=f"{hotel.name[0]}{i+1:02d}",
                price_per_night={'Single': 50, 'Double': 80, 'Deluxe': 120}[room_type],
                capacity={'Single': 1, 'Double': 2, 'Deluxe': 2}[room_type],
                availability=True,
                description=f"Spacious {room_type.lower()} room.",
                room_image_url='https://images.unsplash.com/photo-1611892440504-42a792e24a34?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            )
            print(f'  ✓ Created room: {room.room_number} - {room_type}')

# Create some dummy users if none exist
if User.objects.filter(is_superuser=False).count() < 3:
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    ]
    
    for user_data in users_data:
        if not User.objects.filter(email=user_data['email']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            print(f'✓ Created user: {user.email}')

# Create some dummy bookings if none exist
if Booking.objects.count() < 5:
    users = list(User.objects.filter(is_superuser=False))
    rooms = list(Room.objects.all())
    statuses = ['Pending', 'Confirmed', 'Cancelled']
    
    for i in range(5):
        if users and rooms:
            user = random.choice(users)
            room = random.choice(rooms)
            status = random.choice(statuses)
            
            check_in = date.today() + timedelta(days=random.randint(1, 20))
            check_out = check_in + timedelta(days=random.randint(1, 3))
            
            booking = Booking.objects.create(
                user=user,
                hotel=room.hotel,
                room=room,
                check_in=check_in,
                check_out=check_out,
                total_amount=(check_out - check_in).days * room.price_per_night,
                status=status
            )
            print(f'✓ Created booking: {booking.id} - {status}')

print('\n📊 SUMMARY:')
print(f'   Users: {User.objects.count()}')
print(f'   Hotels: {Hotel.objects.count()}')
print(f'   Rooms: {Room.objects.count()}')
print(f'   Bookings: {Booking.objects.count()}')
print('\n🔑 Admin login: admin@hotel.com / admin123')
