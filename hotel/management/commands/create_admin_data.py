from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hotel.models import Hotel, Room, Booking
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Create dummy data for admin panel testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data for admin panel...')
        
        # Create admin user if not exists
        if not User.objects.filter(email='admin@hotel.com').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@hotel.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write('✓ Created admin user: admin@hotel.com / admin123')
        
        # Create dummy users
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'sarah_jones', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Jones'},
            {'username': 'david_brown', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown'},
            {'username': 'emma_davis', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Davis'},
            {'username': 'chris_miller', 'email': 'chris@example.com', 'first_name': 'Chris', 'last_name': 'Miller'},
            {'username': 'lisa_garcia', 'email': 'lisa@example.com', 'first_name': 'Lisa', 'last_name': 'Garcia'},
        ]
        
        created_users = []
        for user_data in users_data:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                created_users.append(user)
        
        self.stdout.write(f'✓ Created {len(created_users)} dummy users')
        
        # Create dummy hotels
        hotels_data = [
            {
                'name': 'Taj Coromandel Chennai',
                'city': 'Chennai',
                'address': '35, Mahatma Gandhi Road, Nungambakkam, Chennai',
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
                'name': 'The Leela Palace Chennai',
                'city': 'Chennai',
                'address': 'Adyar Gate, MRC Nagar, Chennai',
                'description': 'Luxury and elegance with breathtaking views of the Bay of Bengal.',
                'rating': 4.7,
                'price_range': '$$$$',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
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
                'name': 'The Oberoi Mumbai',
                'city': 'Mumbai',
                'address': 'Mumbai Central, Mumbai',
                'description': 'Sophisticated luxury with panoramic city and sea views.',
                'rating': 4.6,
                'price_range': '$$$$',
                'hotel_image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
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
                'name': 'ITC Gardenia Bangalore',
                'city': 'Bangalore',
                'address': '1, Residency Road, Bangalore',
                'description': 'World-class amenities and exceptional service.',
                'rating': 4.5,
                'price_range': '$$$$',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
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
            if not Hotel.objects.filter(name=hotel_data['name']).exists():
                hotel = Hotel.objects.create(**hotel_data)
                created_hotels.append(hotel)
        
        self.stdout.write(f'✓ Created {len(created_hotels)} dummy hotels')
        
        # Create dummy rooms
        room_types = ['Single', 'Double', 'Deluxe', 'Suite']
        room_images = [
            'https://images.unsplash.com/photo-1611892440504-42a792e24a34?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1596394519210-1b6a7e03d6f9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1584132967334-56e969fb9fc5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        ]
        
        created_rooms = []
        for hotel in created_hotels:
            for i, room_type in enumerate(room_types):
                room_number = f"{hotel.name[0]}{i+1:02d}"
                base_prices = {'Single': 50, 'Double': 80, 'Deluxe': 120, 'Suite': 200}
                city_multiplier = {'Chennai': 1.0, 'Mumbai': 1.3, 'Bangalore': 1.2, 'Delhi': 1.1}
                
                price = base_prices[room_type] * city_multiplier.get(hotel.city, 1.0)
                price = round(price, -1)  # Round to nearest 10
                
                if not Room.objects.filter(hotel=hotel, room_number=room_number).exists():
                    room = Room.objects.create(
                        hotel=hotel,
                        room_type=room_type,
                        room_number=room_number,
                        price_per_night=price,
                        capacity={'Single': 1, 'Double': 2, 'Deluxe': 2, 'Suite': 4}[room_type],
                        availability=True,
                        description=f"Spacious {room_type.lower()} room at {hotel.name}.",
                        room_image_url=room_images[i]
                    )
                    created_rooms.append(room)
        
        self.stdout.write(f'✓ Created {len(created_rooms)} dummy rooms')
        
        # Create dummy bookings
        all_users = list(User.objects.filter(is_superuser=False))
        all_rooms = list(Room.objects.all())
        statuses = ['Pending', 'Confirmed', 'Cancelled']
        
        created_bookings = []
        for i in range(15):  # Create 15 dummy bookings
            if all_users and all_rooms:
                user = random.choice(all_users)
                room = random.choice(all_rooms)
                status = random.choice(statuses)
                
                # Random dates within next 30 days
                check_in = date.today() + timedelta(days=random.randint(1, 25))
                check_out = check_in + timedelta(days=random.randint(1, 5))
                
                # Calculate total amount
                nights = (check_out - check_in).days
                total_amount = nights * room.price_per_night
                
                if not Booking.objects.filter(user=user, room=room, check_in=check_in).exists():
                    booking = Booking.objects.create(
                        user=user,
                        hotel=room.hotel,
                        room=room,
                        check_in=check_in,
                        check_out=check_out,
                        total_amount=total_amount,
                        status=status
                    )
                    created_bookings.append(booking)
        
        self.stdout.write(f'✓ Created {len(created_bookings)} dummy bookings')
        
        # Summary
        self.stdout.write('\n📊 DUMMY DATA SUMMARY:')
        self.stdout.write(f'   Users: {User.objects.count()}')
        self.stdout.write(f'   Hotels: {Hotel.objects.count()}')
        self.stdout.write(f'   Rooms: {Room.objects.count()}')
        self.stdout.write(f'   Bookings: {Booking.objects.count()}')
        self.stdout.write('\n✅ Dummy data creation completed!')
        self.stdout.write('🔑 Admin login: admin@hotel.com / admin123')
