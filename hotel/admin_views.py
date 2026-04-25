from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Hotel, Room, Booking
from .admin_forms import HotelForm, RoomForm
from datetime import datetime, timedelta
import random

def create_dummy_rooms_data():
    """Create dummy room data if no rooms exist"""
    # Get existing hotels or create dummy ones
    hotels = Hotel.objects.all()
    if not hotels.exists():
        # Create dummy hotels first
        hotels_data = [
            {
                'name': 'Taj Mahal Palace',
                'city': 'Mumbai',
                'address': 'Apollo Bandar, Colaba, Mumbai',
                'description': 'Luxury heritage hotel with stunning sea views.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'rating': 4.8
            },
            {
                'name': 'ITC Grand Chola',
                'city': 'Chennai',
                'address': 'Mount Road, Chennai',
                'description': 'Luxury hotel inspired by Chola architecture.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
                'rating': 4.6
            },
            {
                'name': 'The Leela Palace',
                'city': 'Bangalore',
                'address': 'Old Airport Road, Bangalore',
                'description': 'Opulent palace-style hotel with lush gardens.',
                'hotel_image_url': 'https://images.unsplash.com/photo-1582719508461-905324169665?w=800',
                'rating': 4.7
            }
        ]
        
        for hotel_data in hotels_data:
            hotel = Hotel.objects.create(**hotel_data)
            hotels = list(hotels) + [hotel]
    
    # Create dummy rooms
    room_types = ['Single', 'Double', 'Deluxe', 'Suite']
    room_data_templates = [
        {'type': 'Single', 'base_price': 2000, 'capacity': 1, 'description': 'Comfortable single room with basic amenities'},
        {'type': 'Double', 'base_price': 3500, 'capacity': 2, 'description': 'Spacious double room with modern facilities'},
        {'type': 'Deluxe', 'base_price': 5000, 'capacity': 2, 'description': 'Premium deluxe room with luxury amenities'},
        {'type': 'Suite', 'base_price': 8000, 'capacity': 3, 'description': 'Elegant suite with separate living area'}
    ]
    
    room_images = [
        'https://images.unsplash.com/photo-1611892440504-42a792e24a32?w=800',
        'https://images.unsplash.com/photo-1631049307264-da0ec9d70d04?w=800',
        'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800',
        'https://images.unsplash.com/photo-1566665799934-7857372a5b92?w=800'
    ]
    
    created_rooms = 0
    for hotel in hotels:
        for i, template in enumerate(room_data_templates):
            # Create 2-3 rooms of each type per hotel
            for j in range(random.randint(2, 3)):
                room_number = f"{random.choice(['A', 'B', 'C'])}{random.randint(100, 999)}"
                
                # Check if room number already exists for this hotel
                while Room.objects.filter(hotel=hotel, room_number=room_number).exists():
                    room_number = f"{random.choice(['A', 'B', 'C'])}{random.randint(100, 999)}"
                
                room = Room.objects.create(
                    hotel=hotel,
                    room_number=room_number,
                    room_type=template['type'],
                    price_per_night=template['base_price'] + random.randint(-500, 1000),
                    capacity=template['capacity'],
                    availability=random.choice([True, True, True, False]),
                    room_image_url=random.choice(room_images),
                    description=template['description']
                )
                created_rooms += 1
    
    return created_rooms

def admin_login(request):
    """Admin login page"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_panel:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, 'Welcome to Admin Panel!')
            return redirect('admin_panel:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'admin/admin_login.html')

def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_panel:admin_login')

@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:admin_login')
    
    # Get statistics
    stats = {
        'total_hotels': Hotel.objects.count(),
        'total_rooms': Room.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_users': User.objects.count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'confirmed_bookings': Booking.objects.filter(status='Confirmed').count(),
        'cancelled_bookings': Booking.objects.filter(status='Cancelled').count(),
    }
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related('user', 'room', 'hotel').order_by('-created_at')[:10]
    
    # Recent users
    recent_users = User.objects.all().order_by('-date_joined')[:10]
    
    # Monthly revenue (from confirmed bookings)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_revenue = Booking.objects.filter(
        status='Confirmed',
        created_at__year=current_year,
        created_at__month=current_month
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        **stats,
        'recent_bookings': recent_bookings,
        'recent_users': recent_users,
        'monthly_revenue': monthly_revenue,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
def admin_hotels(request):
    """Hotel management page"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    hotels = Hotel.objects.all().order_by('name')
    paginator = Paginator(hotels, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/admin_hotels.html', {'page_obj': page_obj})

@login_required
def admin_add_hotel(request):
    """Add new hotel"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save()
            messages.success(request, f'Hotel "{hotel.name}" added successfully!')
            return redirect('admin_panel:admin_hotels')
    else:
        form = HotelForm()
    
    return render(request, 'admin/admin_hotel_form.html', {
        'form': form,
        'title': 'Add Hotel',
        'action': 'Add'
    })

@login_required
def admin_edit_hotel(request, hotel_id):
    """Edit existing hotel"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            hotel = form.save()
            messages.success(request, f'Hotel "{hotel.name}" updated successfully!')
            return redirect('admin_panel:admin_hotels')
    else:
        form = HotelForm(instance=hotel)
    
    return render(request, 'admin/admin_hotel_form.html', {
        'form': form,
        'hotel': hotel,
        'title': 'Edit Hotel',
        'action': 'Update'
    })

@login_required
def admin_delete_hotel(request, hotel_id):
    """Delete hotel"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    if request.method == 'POST':
        hotel_name = hotel.name
        hotel.delete()
        messages.success(request, f'Hotel "{hotel_name}" deleted successfully!')
        return redirect('admin_panel:admin_hotels')
    
    return render(request, 'admin/admin_delete_confirm.html', {
        'object': hotel,
        'object_type': 'Hotel',
        'cancel_url': 'admin_panel:admin_hotels'
    })

@login_required
def admin_rooms(request):
    """Room management page"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    rooms = Room.objects.select_related('hotel').all().order_by('hotel__name', 'room_number')
    paginator = Paginator(rooms, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_rooms = rooms.count()
    available_rooms = rooms.filter(availability=True).count()
    unavailable_rooms = rooms.filter(availability=False).count()
    
    # Calculate room type distribution
    room_types = {}
    for room_type_choice in Room.ROOM_TYPES:
        room_type_name = room_type_choice[0]
        room_type_count = rooms.filter(room_type=room_type_name).count()
        room_types[room_type_name] = room_type_count
    
    # Get hotels with rooms count
    hotels_with_rooms = rooms.values('hotel__name').distinct().count()
    
    # If no rooms exist, create dummy data
    if total_rooms == 0:
        create_dummy_rooms_data()
        # Refresh the data after creating dummy rooms
        rooms = Room.objects.select_related('hotel').all().order_by('hotel__name', 'room_number')
        paginator = Paginator(rooms, 15)
        page_obj = paginator.get_page(page_number)
        
        total_rooms = rooms.count()
        available_rooms = rooms.filter(availability=True).count()
        unavailable_rooms = rooms.filter(availability=False).count()
        
        for room_type_choice in Room.ROOM_TYPES:
            room_type_name = room_type_choice[0]
            room_type_count = rooms.filter(room_type=room_type_name).count()
            room_types[room_type_name] = room_type_count
        
        hotels_with_rooms = rooms.values('hotel__name').distinct().count()
    
    context = {
        'page_obj': page_obj,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'unavailable_rooms': unavailable_rooms,
        'room_types': room_types,
        'hotels_with_rooms': hotels_with_rooms,
    }
    
    return render(request, 'admin/admin_rooms.html', context)

@login_required
def admin_add_room(request):
    """Add new room"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room "{room.room_number}" added successfully!')
            return redirect('admin_panel:admin_rooms')
    else:
        form = RoomForm()
    
    return render(request, 'admin/admin_room_form.html', {
        'form': form,
        'title': 'Add Room',
        'action': 'Add'
    })

@login_required
def admin_edit_room(request, room_id):
    """Edit existing room"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room "{room.room_number}" updated successfully!')
            return redirect('admin_panel:admin_rooms')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'admin/admin_room_form.html', {
        'form': form,
        'room': room,
        'title': 'Edit Room',
        'action': 'Update'
    })

@login_required
def admin_delete_room(request, room_id):
    """Delete room"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        room_number = room.room_number
        room.delete()
        messages.success(request, f'Room "{room_number}" deleted successfully!')
        return redirect('admin_panel:admin_rooms')
    
    return render(request, 'admin/admin_delete_confirm.html', {
        'object': room,
        'object_type': 'Room',
        'cancel_url': 'admin_panel:admin_rooms'
    })

@login_required
def admin_bookings(request):
    """Booking management page"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    # Get real bookings from database
    bookings_qs = Booking.objects.select_related('user', 'room', 'hotel').order_by('-created_at')
    
    # Calculate booking statistics in view (not template)
    total_bookings = bookings_qs.count()
    pending_bookings = bookings_qs.filter(status='Pending').count()
    confirmed_bookings = bookings_qs.filter(status='Confirmed').count()
    cancelled_bookings = bookings_qs.filter(status='Cancelled').count()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        bookings_qs = bookings_qs.filter(status=status_filter)
    
    # Create pagination
    from django.core.paginator import Paginator
    paginator = Paginator(bookings_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/admin_bookings.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'status_choices': Booking.STATUS_CHOICES,
        # Statistics calculated in view
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
    })

@login_required
def admin_confirm_booking(request, booking_id):
    """Confirm booking"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Confirmed'
    booking.save()
    messages.success(request, f'Booking #{booking.id} confirmed successfully!')
    return redirect('admin_panel:admin_bookings')

@login_required
def admin_cancel_booking(request, booking_id):
    """Cancel booking"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'
    booking.save()
    messages.success(request, f'Booking #{booking.id} cancelled successfully!')
    return redirect('admin_panel:admin_bookings')

@login_required
def admin_pending_booking(request, booking_id):
    """Mark booking as pending"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Pending'
    booking.save()
    messages.success(request, f'Booking #{booking.id} marked as pending!')
    return redirect('admin_panel:admin_bookings')

@login_required
def admin_delete_booking(request, booking_id):
    """Delete booking"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        booking_id = booking.id
        booking.delete()
        messages.success(request, f'Booking #{booking_id} deleted successfully!')
        return redirect('admin_panel:admin_bookings')
    
    return render(request, 'admin/admin_delete_confirm.html', {
        'object': booking,
        'object_type': 'Booking',
        'cancel_url': 'admin_panel:admin_bookings'
    })

@login_required
def admin_users(request):
    """User management page"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    # Get all users with their bookings
    users = User.objects.prefetch_related('bookings').order_by('-date_joined')
    
    # Build users_with_stats list in view (not template)
    users_with_stats = []
    for user in users:
        total_bookings = user.bookings.count()
        latest_booking = user.bookings.first() if user.bookings.exists() else None
        
        users_with_stats.append({
            'user': user,
            'total_bookings': total_bookings,
            'latest_booking': latest_booking,
        })
    
    # Sort users by total bookings (most active first) - done in Python
    most_active_users = sorted(users_with_stats, key=lambda x: x['total_bookings'], reverse=True)[:5]
    
    # Calculate user statistics
    active_users_count = len([u for u in users_with_stats if u['user'].is_active])
    inactive_users_count = len([u for u in users_with_stats if not u['user'].is_active])
    staff_users_count = len([u for u in users_with_stats if u['user'].is_staff])
    
    # Create pagination for the main users list
    from django.core.paginator import Paginator
    paginator = Paginator(users_with_stats, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/admin_users.html', {
        'page_obj': page_obj,
        'most_active_users': most_active_users,
        'active_users_count': active_users_count,
        'inactive_users_count': inactive_users_count,
        'staff_users_count': staff_users_count,
    })

@login_required
def admin_toggle_user(request, user_id):
    """Toggle user active status"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f'User "{user.username}" {status} successfully!')
    return redirect('admin_panel:admin_users')

@login_required
def admin_delete_user(request, user_id):
    """Delete user"""
    if not request.user.is_superuser:
        return redirect('admin_panel:admin_login')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
        return redirect('admin_panel:admin_users')
    
    return render(request, 'admin/admin_delete_confirm.html', {
        'object': user,
        'object_type': 'User',
        'cancel_url': 'admin_panel:admin_users'
    })
