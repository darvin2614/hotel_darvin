from django.core.management.base import BaseCommand
from hotel.models import Hotel, Room


class Command(BaseCommand):
    help = 'Create dummy data for hotels and rooms'

    def handle(self, *args, **options):
        # Clear existing data
        Hotel.objects.all().delete()
        Room.objects.all().delete()
        
        # Hotels data - Correct city-specific hotel names with hotel-style images
        hotels_data = [
            # Chennai Hotels
            {
                'name': 'Taj Coromandel Chennai',
                'city': 'Chennai',
                'address': '35, Mahatma Gandhi Road, Nungambakkam, Chennai, Tamil Nadu 600034',
                'description': 'Taj Coromandel Chennai offers luxury accommodation with contemporary design and traditional South Indian hospitality.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.5,
                'price_range': '$$$$'
            },
            {
                'name': 'ITC Grand Chola Chennai',
                'city': 'Chennai',
                'address': '63, Mount Road, Chennai, Tamil Nadu 600002',
                'description': 'ITC Grand Chola Chennai is a magnificent luxury hotel inspired by Dravidian architecture of the Chola dynasty.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.6,
                'price_range': '$$$$'
            },
            {
                'name': 'The Leela Palace Chennai',
                'city': 'Chennai',
                'address': 'Adyar Gate, MRC Nagar, Chennai, Tamil Nadu 600028',
                'description': 'The Leela Palace Chennai combines luxury and elegance with breathtaking views of the Bay of Bengal.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.7,
                'price_range': '$$$$'
            },
            {
                'name': 'Radisson Blu Chennai',
                'city': 'Chennai',
                'address': '265, GST Road, Chennai, Tamil Nadu 600034',
                'description': 'Radisson Blu Chennai provides modern luxury accommodation with excellent business facilities.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.3,
                'price_range': '$$$'
            },
            {
                'name': 'Park Hyatt Chennai',
                'city': 'Chennai',
                'address': '39, Velachery Road, Chennai, Tamil Nadu 600042',
                'description': 'Park Hyatt Chennai offers sophisticated luxury with world-class amenities and exceptional service.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1571003163706-1cc6e0132721?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.4,
                'price_range': '$$$$'
            },
            
            # Mumbai Hotels
            {
                'name': 'Taj Mahal Palace Mumbai',
                'city': 'Mumbai',
                'address': 'Apollo Bandar, Colaba, Mumbai, Maharashtra 400001',
                'description': 'The iconic Taj Mahal Palace Mumbai is a luxurious heritage hotel offering stunning views of the Arabian Sea.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.8,
                'price_range': '$$$$'
            },
            {
                'name': 'The Oberoi Mumbai',
                'city': 'Mumbai',
                'address': 'Mumbai Central, Mumbai, Maharashtra 400008',
                'description': 'The Oberoi Mumbai offers sophisticated luxury with panoramic views of the Arabian Sea and city skyline.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.6,
                'price_range': '$$$$'
            },
            {
                'name': 'Trident Nariman Point Mumbai',
                'city': 'Mumbai',
                'address': 'Nariman Point, Mumbai, Maharashtra 400021',
                'description': 'Trident Nariman Point Mumbai offers luxurious accommodation with stunning sea views and world-class dining.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.4,
                'price_range': '$$$$'
            },
            {
                'name': 'ITC Maratha Mumbai',
                'city': 'Mumbai',
                'address': '221, Dr. Annie Besant Road, Worli, Mumbai, Maharashtra 400018',
                'description': 'ITC Maratha Mumbai offers luxury accommodation with modern amenities and exceptional service.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.3,
                'price_range': '$$$'
            },
            {
                'name': 'Grand Hyatt Mumbai',
                'city': 'Mumbai',
                'address': 'Sahar Airport Road, Mumbai, Maharashtra 400059',
                'description': 'Grand Hyatt Mumbai offers world-class luxury accommodation with exceptional amenities and service.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.5,
                'price_range': '$$$$'
            },
            
            # Bangalore Hotels
            {
                'name': 'The Leela Palace Bangalore',
                'city': 'Bangalore',
                'address': '23, Old Airport Road, HAL 2nd Stage, Bangalore, Karnataka 560008',
                'description': 'The Leela Palace Bangalore is a luxurious hotel that combines royal charm with modern amenities.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.7,
                'price_range': '$$$$'
            },
            {
                'name': 'ITC Gardenia Bangalore',
                'city': 'Bangalore',
                'address': '1, Residency Road, Bangalore, Karnataka 560025',
                'description': 'ITC Gardenia Bangalore is a luxury hotel offering world-class amenities and exceptional service.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.5,
                'price_range': '$$$$'
            },
            {
                'name': 'Taj West End Bangalore',
                'city': 'Bangalore',
                'address': '22, Race Course Road, Bangalore, Karnataka 560001',
                'description': 'Taj West End Bangalore is a heritage hotel offering luxury accommodation amidst lush greenery.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1571003163706-1cc6e0132721?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.4,
                'price_range': '$$$$'
            },
            {
                'name': 'The Oberoi Bangalore',
                'city': 'Bangalore',
                'address': '88, MG Road, Bangalore, Karnataka 560001',
                'description': 'The Oberoi Bangalore offers sophisticated luxury with world-class amenities in the heart of the city.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.6,
                'price_range': '$$$$'
            },
            {
                'name': 'Shangri-La Bangalore',
                'city': 'Bangalore',
                'address': '56, Palace Road, Bangalore, Karnataka 560001',
                'description': 'Shangri-La Bangalore offers luxury accommodation with world-class amenities and exceptional service.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.3,
                'price_range': '$$$'
            },
            
            # Delhi Hotels
            {
                'name': 'The Leela Palace New Delhi',
                'city': 'Delhi',
                'address': 'Chanakyapuri, New Delhi, Delhi 110021',
                'description': 'The Leela Palace New Delhi offers luxurious accommodation with world-class amenities in the diplomatic enclave.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.7,
                'price_range': '$$$$'
            },
            {
                'name': 'ITC Maurya Delhi',
                'city': 'Delhi',
                'address': 'Diplomatic Enclave, Chanakyapuri, New Delhi, Delhi 110021',
                'description': 'ITC Maurya Delhi is a luxury hotel offering world-class amenities and exceptional service in the diplomatic area.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.6,
                'price_range': '$$$$'
            },
            {
                'name': 'The Lalit New Delhi',
                'city': 'Delhi',
                'address': 'Barakhamba Avenue, Connaught Place, New Delhi, Delhi 110001',
                'description': 'The Lalit New Delhi is a luxury hotel offering world-class amenities and exceptional service in the heart of the capital.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.3,
                'price_range': '$$$$'
            },
            {
                'name': 'Taj Palace New Delhi',
                'city': 'Delhi',
                'address': '2, Man Singh Road, New Delhi, Delhi 110001',
                'description': 'Taj Palace New Delhi offers luxury accommodation with world-class amenities in the heart of the capital.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.5,
                'price_range': '$$$$'
            },
            {
                'name': 'The Oberoi New Delhi',
                'city': 'Delhi',
                'address': 'Dr. Zakir Hussain Marg, New Delhi, Delhi 110003',
                'description': 'The Oberoi New Delhi offers sophisticated luxury with world-class amenities in the heart of the capital.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'rating': 4.6,
                'price_range': '$$$$'
            }
        ]

        # Room types and their base prices
        room_types = [
            {'type': 'Single', 'base_price': 50, 'capacity': 1},
            {'type': 'Double', 'base_price': 80, 'capacity': 2},
            {'type': 'Deluxe', 'base_price': 120, 'capacity': 2},
            {'type': 'Suite', 'base_price': 200, 'capacity': 4}
        ]

        # Room descriptions
        room_descriptions = {
            'Single': 'Comfortable single room perfect for solo travelers. Features a cozy bed, work desk, and modern amenities.',
            'Double': 'Spacious double room ideal for couples or friends. Features a comfortable double bed and elegant decor.',
            'Deluxe': 'Luxurious deluxe room with premium amenities. Features a king-size bed, seating area, and city views.',
            'Suite': 'Exquisite suite offering ultimate luxury. Features separate living area, bedroom, and premium facilities.'
        }

        created_hotels = []
        
        # Create hotels
        for hotel_data in hotels_data:
            hotel = Hotel.objects.create(**hotel_data)
            created_hotels.append(hotel)
            self.stdout.write(
                self.style.SUCCESS(f'Created hotel: {hotel.name} in {hotel.city}')
            )

        # Create rooms for each hotel with room-style images
        room_image_sets = [
            [
                'https://images.unsplash.com/photo-1611892440504-42a792e24a34?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Single room
                'https://images.unsplash.com/photo-1596394519210-1b6a7e03d6f9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Double room
                'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Deluxe room
                'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'   # Suite room
            ],
            [
                'https://images.unsplash.com/photo-1590490374829-535513e4594c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Single room
                'https://images.unsplash.com/photo-1618774921380-9f6893a2e1a3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Double room
                'https://images.unsplash.com/photo-1584132967334-56e969fb9fc5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Deluxe room
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'   # Suite room
            ],
            [
                'https://images.unsplash.com/photo-1566665747-3d5b594c9eb1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Single room
                'https://images.unsplash.com/photo-1598928506311-c55ded91e20b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Double room
                'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Deluxe room
                'https://images.unsplash.com/photo-1571003163706-1cc6e0132721?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'   # Suite room
            ],
            [
                'https://images.unsplash.com/photo-1631049307591-661888f94f0d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Single room
                'https://images.unsplash.com/photo-1613475504966-7e56260bfed5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Double room
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Deluxe room
                'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'   # Suite room
            ],
            [
                'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Single room
                'https://images.unsplash.com/photo-1564501049412-a61e8d5b8b4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Double room
                'https://images.unsplash.com/photo-1596394519210-1b6a7e03d6f9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Deluxe room
                'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'   # Suite room
            ]
        ]
        
        for hotel in created_hotels:
            image_set = room_image_sets[created_hotels.index(hotel) % len(room_image_sets)]
            for i, room_type in enumerate(room_types):
                # City-based price adjustment
                city_multiplier = {
                    'Chennai': 1.0,
                    'Mumbai': 1.3,
                    'Bangalore': 1.2,
                    'Delhi': 1.1
                }
                
                # Rating-based price adjustment
                rating_multiplier = hotel.rating / 4.0
                
                # Calculate final price
                base_price = room_type['base_price']
                city_price = base_price * city_multiplier.get(hotel.city, 1.0)
                final_price = city_price * rating_multiplier
                final_price = round(final_price, -1)  # Round to nearest 10
                
                # Create room with unique room image
                room = Room.objects.create(
                    hotel=hotel,
                    room_type=room_type['type'],
                    price_per_night=final_price,
                    capacity=room_type['capacity'],
                    availability=True,
                    description=f"Spacious {room_type['type'].lower()} room with modern amenities at {hotel.name}.",
                    room_image_url=image_set[i]
                )
                
                self.stdout.write(f"Created {room_type['type']} room for {hotel.name}")
        
        # Display summary
        total_hotels = Hotel.objects.count()
        total_rooms = Room.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Total: {total_hotels} hotels, {total_rooms} rooms')
        )
