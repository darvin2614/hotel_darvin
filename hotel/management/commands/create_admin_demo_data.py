from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random
from hotel.models import Hotel, Room, Booking

class Command(BaseCommand):
    help = 'Create demo data for the admin panel'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data for admin panel...')
        
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@hotel.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created (admin/admin123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Admin user already exists'))
        
        # Create demo hotels
        hotels_data = [
            {
                'name': 'Taj Mahal Palace',
                'city': 'Mumbai',
                'address': 'Apollo Bandar, Colaba, Mumbai',
                'description': 'Luxury heritage hotel with stunning sea views and world-class amenities.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'rating': 4.8
            },
            {
                'name': 'ITC Grand Chola',
                'city': 'Chennai',
                'address': 'Mount Road, Chennai',
                'description': 'Luxury hotel inspired by Chola architecture with modern facilities.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
                'rating': 4.6
            },
            {
                'name': 'The Leela Palace',
                'city': 'Bangalore',
                'address': 'Old Airport Road, Bangalore',
                'description': 'Opulent palace-style hotel with lush gardens and premium services.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1582719508461-905324169665?w=800',
                'rating': 4.7
            },
            {
                'name': 'The Oberoi',
                'city': 'New Delhi',
                'address': 'Dr. Zakir Hussain Marg, New Delhi',
                'description': 'Elegant luxury hotel with panoramic views of Delhi\'s golf course.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-4a2db3b964e5?w=800',
                'rating': 4.5
            },
            {
                'name': 'Marina Bay Sands',
                'city': 'Mumbai',
                'address': 'Worli Sea Face, Mumbai',
                'description': 'Modern luxury hotel with rooftop infinity pool and city views.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
                'rating': 4.9
            }
        ]
        
        created_hotels = []
        for hotel_data in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            created_hotels.append(hotel)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Hotel created: {hotel.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Hotel already exists: {hotel.name}'))
        
        # Create demo rooms
        room_types = ['Single', 'Double', 'Deluxe', 'Suite', 'Penthouse']
        room_data_templates = [
            {'type': 'Single', 'price': 2000, 'capacity': 1, 'description': 'Comfortable single room with basic amenities'},
            {'type': 'Double', 'price': 3500, 'capacity': 2, 'description': 'Spacious double room with modern facilities'},
            {'type': 'Deluxe', 'price': 5000, 'capacity': 2, 'description': 'Premium deluxe room with luxury amenities'},
            {'type': 'Suite', 'price': 8000, 'capacity': 3, 'description': 'Elegant suite with separate living area'},
            {'type': 'Penthouse', 'price': 15000, 'capacity': 4, 'description': 'Ultra-luxury penthouse with panoramic views'}
        ]
        
        room_images = [
            'https://images.unsplash.com/photo-1611892440504-42a792e24a32?w=800',
            'https://images.unsplash.com/photo-1631049307264-da0ec9d70d04?w=800',
            'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800',
            'https://images.unsplash.com/photo-1566665799934-7857372a5b92?w=800',
            'https://images.unsplash.com/photo-1590490360238-c7b52160eadc?w=800'
        ]
        
        created_rooms = []
        for hotel in created_hotels:
            for i, template in enumerate(room_data_templates):
                room_number = f"{random.choice(['A', 'B', 'C'])}{random.randint(100, 999)}"
                room, created = Room.objects.get_or_create(
                    hotel=hotel,
                    room_number=room_number,
                    defaults={
                        'room_type': template['type'],
                        'price_per_night': template['price'] + random.randint(-500, 1000),
                        'capacity': template['capacity'],
                        'availability': random.choice([True, True, True, False]),
                        'room_image_url': random.choice(room_images),
                        'description': template['description']
                    }
                )
                created_rooms.append(room)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Room created: {room.room_number} - {hotel.name}'))
        
        # Create demo users
        demo_users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'sarah_jones', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Jones'},
            {'username': 'alex_brown', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Brown'},
        ]
        
        demo_users = []
        for user_data in demo_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'password': 'user123'
                }
            )
            if created:
                user.set_password('user123')
                user.save()
                demo_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'✓ User created: {user.username} (user123)'))
            else:
                demo_users.append(user)
                self.stdout.write(self.style.WARNING(f'⚠ User already exists: {user.username}'))
        
        # Create demo bookings
        if created_rooms and demo_users:
            booking_statuses = ['Pending', 'Confirmed', 'Cancelled']
            created_bookings = 0
            
            for i in range(20):  # Create 20 demo bookings
                room = random.choice(created_rooms)
                user = random.choice(demo_users)
                
                # Random check-in and check-out dates
                check_in = timezone.now().date() + timedelta(days=random.randint(-10, 30))
                check_out = check_in + timedelta(days=random.randint(1, 7))
                
                # Calculate total amount
                nights = (check_out - check_in).days
                total_amount = room.price_per_night * nights
                
                booking, created = Booking.objects.get_or_create(
                    user=user,
                    room=room,
                    check_in=check_in,
                    check_out=check_out,
                    defaults={
                        'hotel': room.hotel,
                        'total_amount': total_amount,
                        'status': random.choice(booking_statuses),
                        'created_at': timezone.now() - timedelta(days=random.randint(0, 30))
                    }
                )
                
                if created:
                    created_bookings += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Booking created: #{booking.id} - {user.username}'))
            
            if created_bookings == 0:
                self.stdout.write(self.style.WARNING('⚠ All demo bookings already exist'))
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 Demo data creation completed!'))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('  Admin: admin/admin123')
        self.stdout.write('  Users: user123 (for all demo users)')
        self.stdout.write('\nStatistics:')
        self.stdout.write(f'  Hotels: {Hotel.objects.count()}')
        self.stdout.write(f'  Rooms: {Room.objects.count()}')
        self.stdout.write(f'  Users: {User.objects.count()}')
        self.stdout.write(f'  Bookings: {Booking.objects.count()}')
        self.stdout.write('\nAdmin Panel URL:')
        self.stdout.write('  http://127.0.0.1:8000/admin-panel/login/')
        self.stdout.write('='*50)
