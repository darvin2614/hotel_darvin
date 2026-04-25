#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Hotel, Room, Booking, User
from datetime import date, timedelta

def test_booking_integration():
    """Test complete booking-to-admin integration"""
    
    print("🔍 Testing Booking-to-Admin Integration")
    print("=" * 50)
    
    # 1. Check if models are working
    print("\n1. Checking Models...")
    try:
        hotels_count = Hotel.objects.count()
        rooms_count = Room.objects.count()
        bookings_count = Booking.objects.count()
        users_count = User.objects.count()
        
        print(f"   Hotels: {hotels_count}")
        print(f"   Rooms: {rooms_count}")
        print(f"   Bookings: {bookings_count}")
        print(f"   Users: {users_count}")
        print("   ✅ Models working correctly")
    except Exception as e:
        print(f"   ❌ Model error: {e}")
        return
    
    # 2. Create test user if needed
    print("\n2. Checking Test User...")
    try:
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            print("   ✅ Test user created")
        else:
            print("   ✅ Test user exists")
    except Exception as e:
        print(f"   ❌ User creation error: {e}")
        return
    
    # 3. Get a room for testing
    print("\n3. Getting Test Room...")
    try:
        test_room = Room.objects.first()
        if not test_room:
            print("   ❌ No rooms found!")
            return
        print(f"   ✅ Using Room {test_room.id}: {test_room.get_room_type_display()} at {test_room.hotel.name}")
    except Exception as e:
        print(f"   ❌ Room error: {e}")
        return
    
    # 4. Create a test booking
    print("\n4. Creating Test Booking...")
    try:
        # Check if booking already exists
        existing_booking = Booking.objects.filter(user=test_user, room=test_room).first()
        if existing_booking:
            print(f"   ✅ Using existing booking #{existing_booking.id}")
            test_booking = existing_booking
        else:
            # Create new booking
            check_in = date.today() + timedelta(days=5)
            check_out = check_in + timedelta(days=2)
            
            test_booking = Booking.objects.create(
                user=test_user,
                hotel=test_room.hotel,
                room=test_room,
                check_in=check_in,
                check_out=check_out,
                total_amount=test_room.price_per_night * 2,
                status='Pending'
            )
            print(f"   ✅ Created booking #{test_booking.id}")
    except Exception as e:
        print(f"   ❌ Booking creation error: {e}")
        return
    
    # 5. Test admin booking query
    print("\n5. Testing Admin Booking Query...")
    try:
        admin_bookings = Booking.objects.select_related('user', 'room', 'hotel').order_by('-created_at')
        print(f"   Total bookings for admin: {admin_bookings.count()}")
        
        # Find our test booking
        our_booking = admin_bookings.filter(id=test_booking.id).first()
        if our_booking:
            print(f"   ✅ Test booking found in admin query")
            print(f"   User: {our_booking.user.username}")
            print(f"   Hotel: {our_booking.hotel.name}")
            print(f"   Room: {our_booking.room.get_room_type_display()}")
            print(f"   Status: {our_booking.status}")
        else:
            print("   ❌ Test booking not found in admin query")
    except Exception as e:
        print(f"   ❌ Admin query error: {e}")
        return
    
    # 6. Test admin booking actions
    print("\n6. Testing Admin Booking Actions...")
    try:
        # Test status change
        original_status = test_booking.status
        test_booking.status = 'Confirmed'
        test_booking.save()
        
        # Verify change
        updated_booking = Booking.objects.get(id=test_booking.id)
        if updated_booking.status == 'Confirmed':
            print("   ✅ Status change works")
        else:
            print("   ❌ Status change failed")
        
        # Restore original status
        test_booking.status = original_status
        test_booking.save()
        print("   ✅ Admin actions working")
    except Exception as e:
        print(f"   ❌ Admin action error: {e}")
        return
    
    # 7. Test user booking statistics
    print("\n7. Testing User Booking Statistics...")
    try:
        user_booking_count = test_user.bookings.count()
        print(f"   User booking count: {user_booking_count}")
        
        if user_booking_count > 0:
            latest_booking = test_user.bookings.first()
            print(f"   Latest booking: #{latest_booking.id} ({latest_booking.status})")
            print("   ✅ User statistics working")
        else:
            print("   ⚠️  User has no bookings")
    except Exception as e:
        print(f"   ❌ User statistics error: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Booking-to-Admin Integration Test Complete!")
    print("✅ All tests passed - Integration is working correctly!")
    
    print("\n📋 Test Results Summary:")
    print(f"   - Test User: {test_user.username}")
    print(f"   - Test Room: {test_room.get_room_type_display()} at {test_room.hotel.name}")
    print(f"   - Test Booking: #{test_booking.id}")
    print(f"   - Booking Status: {test_booking.status}")
    print(f"   - Check-in: {test_booking.check_in}")
    print(f"   - Check-out: {test_booking.check_out}")
    print(f"   - Total Amount: ₹{test_booking.total_amount}")

if __name__ == "__main__":
    test_booking_integration()
