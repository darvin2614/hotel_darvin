from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from .models import Hotel, Room, Booking
from .forms import CustomUserCreationForm, LoginForm, BookingForm, HotelSearchForm


def home(request):
    """Home page with featured hotels"""
    # Optimized: Use select_related and only() for better performance
    featured_hotels = Hotel.objects.only('id', 'name', 'city', 'hotel_image_url', 'rating').select_related()[:6]
    
    # Use a single query for counts instead of multiple
    stats = Hotel.objects.aggregate(
        total_hotels=Count('id'),
        total_rooms=Count('rooms')
    )
    
    context = {
        'featured_hotels': featured_hotels,
        'total_hotels': stats['total_hotels'],
        'total_rooms': stats['total_rooms'],
    }
    return render(request, 'hotel/home.html', context)


def hotel_list(request):
    """Hotel listing page with search and filter"""
    form = HotelSearchForm(request.GET or None)
    
    # Optimized: Use only() to load only needed fields
    hotels = Hotel.objects.only('id', 'name', 'city', 'hotel_image_url', 'rating', 'price_range')
    
    if form.is_valid():
        city = form.cleaned_data.get('city')
        hotel_name = form.cleaned_data.get('hotel_name')
        
        if city:
            hotels = hotels.filter(city__icontains=city)
        if hotel_name:
            hotels = hotels.filter(name__icontains=hotel_name)
    
    # Get unique cities for filter - optimized query
    cities = Hotel.objects.values_list('city', flat=True).distinct().order_by('city')
    
    context = {
        'hotels': hotels,
        'form': form,
        'cities': cities,
    }
    return render(request, 'hotel/hotel_list.html', context)


def hotel_detail(request, hotel_id):
    """Hotel detail page with rooms"""
    hotel = get_object_or_404(Hotel, id=hotel_id)
    # Optimized: Use select_related to avoid N+1 queries
    rooms = hotel.rooms.filter(availability=True).select_related('hotel')
    
    context = {
        'hotel': hotel,
        'rooms': rooms,
    }
    return render(request, 'hotel/hotel_detail.html', context)


def room_detail(request, room_id):
    """Room detail page"""
    # Optimized: Use select_related to avoid N+1 queries
    room = get_object_or_404(Room.objects.select_related('hotel'), id=room_id)
    
    context = {
        'room': room,
    }
    return render(request, 'hotel/room_detail.html', context)


def booking_page(request, room_id):
    """Booking page for a specific room"""
    # Check if user is authenticated, if not redirect to login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to continue with booking.')
        return redirect(f'/login/?next=/booking/{room_id}/')
    
    # Optimized: Use select_related to avoid N+1 queries
    room = get_object_or_404(Room.objects.select_related('hotel'), id=room_id)
    
    if not room.availability:
        messages.error(request, 'This room is not available for booking.')
        return redirect('room_detail', room_id=room_id)
    
    if request.method == 'POST':
        form = BookingForm(room, request.POST)
        print(f"DEBUG: Form submitted - Is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG: Form errors: {form.errors}")
            print(f"DEBUG: Non-field errors: {form.non_field_errors()}")
        
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in']
            check_out_date = form.cleaned_data['check_out']
            
            print(f"DEBUG: Dates - Check-in: {check_in_date}, Check-out: {check_out_date}")
            
            # Additional date validation
            today = date.today()
            if check_in_date < today:
                print("DEBUG: Check-in date is in the past")
                messages.error(request, 'Check-in date cannot be in the past.')
            elif check_out_date <= check_in_date:
                print("DEBUG: Check-out date is not after check-in")
                messages.error(request, 'Check-out date must be after check-in date.')
            else:
                print("DEBUG: Date validation passed, checking availability...")
                # Only check for Confirmed bookings - Pending bookings should not block new bookings
                conflicting_bookings = Booking.objects.filter(
                    room=room,
                    status='Confirmed',  # Only Confirmed bookings block availability
                    check_in__lt=check_out_date,  # existing check-in before new check-out
                    check_out__gt=check_in_date   # existing check-out after new check-in
                )
                
                # DEBUG: Print what we're checking
                print(f"DEBUG: Checking Room {room.id} for {check_in_date} to {check_out_date}")
                print(f"DEBUG: Found {conflicting_bookings.count()} conflicting bookings")
                for conf in conflicting_bookings:
                    print(f"  - {conf.check_in} to {conf.check_out} ({conf.status})")
                
                if not conflicting_bookings.exists():
                    print("DEBUG: No conflicts, proceeding to verification page")
                    # Store booking preview data in session
                    # Convert date objects to strings to fix JSON serialization error
                    booking_preview = {
                        'room_id': room.id,
                        'hotel_id': room.hotel.id,
                        'hotel_name': room.hotel.name,
                        'city': room.hotel.city,
                        'address': room.hotel.address,
                        'room_type': room.room_type,
                        'room_number': room.room_number if hasattr(room, 'room_number') else '',
                        'check_in_date': check_in_date.isoformat(),
                        'check_out_date': check_out_date.isoformat(),
                        'price_per_night': float(room.price_per_night),
                        'total_amount': float(form.calculate_total_amount()),
                        'room_image_url': room.room_image_url,
                        'hotel_image_url': room.hotel.hotel_image_url,
                        'user_email': request.user.email,
                    }
                    request.session['booking_preview'] = booking_preview
                    request.session.modified = True  # Ensure session is saved
                    
                    # Redirect to booking verification page
                    return redirect('booking_verify', room_id=room.id)
                else:
                    print("DEBUG: Found conflicting bookings, showing error")
                    messages.error(request, 'This room is not available for the selected dates.')
        else:
            print("DEBUG: Form submission failed validation")
    else:
        form = BookingForm(room)
    
    context = {
        'room': room,
        'form': form,
    }
    return render(request, 'hotel/booking.html', context)


@login_required
def my_bookings(request):
    """User's bookings page"""
    # Optimized: Use select_related and aggregate in single query
    from django.db.models import Count, Q
    
    user_bookings = Booking.objects.filter(user=request.user).select_related('room', 'room__hotel').order_by('-created_at')
    
    # Get booking counts in a single query
    booking_stats = user_bookings.aggregate(
        total_bookings=Count('id'),
        confirmed_bookings=Count('id', filter=Q(status='Confirmed')),
        pending_bookings=Count('id', filter=Q(status='Pending')),
        cancelled_bookings=Count('id', filter=Q(status='Cancelled')),
    )
    
    context = {
        'bookings': user_bookings,
        **booking_stats,
    }
    return render(request, 'hotel/my_bookings.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.can_cancel:
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('my_bookings')


def signup(request):
    """User registration page"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'hotel/signup.html', {'form': form})


def login_view(request):
    """User login page"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Safely get user by email (handle duplicates)
            user = User.objects.filter(email=email).first()
            if user is None:
                messages.error(request, 'Invalid email or password.')
            else:
                authenticated_user = authenticate(username=user.username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, f'Welcome back, {email}!')
                    
                    # Check for next parameter to redirect back to booking
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'hotel/login.html', {'form': form})


@login_required
def login_verification(request):
    """Login verification page"""
    context = {
    }
    return render(request, 'hotel/login_verification.html', context)


@login_required
def booking_verify(request, room_id):
    """Booking verification page"""
    # Get room details
    room = get_object_or_404(Room, id=room_id)
    
    # Get booking data from form or session
    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        total_amount = request.POST.get('total_amount')
        
        # Store in session for confirmation
        booking_preview = {
            'room_id': room_id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'total_amount': total_amount,
        }
        request.session['booking_preview'] = booking_preview
        request.session.modified = True
    else:
        # Try to get from session first
        booking_preview = request.session.get('booking_preview')
        if not booking_preview or booking_preview.get('room_id') != int(room_id):
            # If no session data, redirect to booking page
            return redirect('booking', room_id=room_id)
        
        check_in_date = booking_preview['check_in_date']
        check_out_date = booking_preview['check_out_date']
        total_amount = booking_preview['total_amount']
    
    # Calculate nights for display
    from datetime import datetime
    if isinstance(check_in_date, str):
        check_in_date_obj = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date_obj = datetime.strptime(check_out_date, '%Y-%m-%d').date()
    else:
        check_in_date_obj = check_in_date
        check_out_date_obj = check_out_date
    
    nights = (check_out_date_obj - check_in_date_obj).days
    
    context = {
        'user': request.user,
        'room': room,
        'hotel': room.hotel,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'total_amount': total_amount,
        'nights': nights,
    }
    return render(request, 'hotel/booking_verify.html', context)


@login_required
def booking_confirm(request, room_id):
    """Confirm and save booking"""
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('booking_verify', room_id=room_id)
    
    # Get room
    room = get_object_or_404(Room, id=room_id)
    
    # Get form data
    check_in_date = request.POST.get('check_in_date')
    check_out_date = request.POST.get('check_out_date')
    total_amount = request.POST.get('total_amount')
    
    if not all([check_in_date, check_out_date, total_amount]):
        messages.error(request, 'Missing booking information.')
        return redirect('booking_verify', room_id=room_id)
    
    try:
        # Convert string dates to date objects
        from datetime import datetime
        check_in_date_obj = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date_obj = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        
        # Validate dates
        if check_in_date_obj >= check_out_date_obj:
            messages.error(request, 'Check-out date must be after check-in date.')
            return redirect('booking_verify', room_id=room_id)
        
        if check_in_date_obj < datetime.now().date():
            messages.error(request, 'Check-in date cannot be in the past.')
            return redirect('booking_verify', room_id=room_id)
        
        # Double-check availability before creating booking
        conflicting_bookings = Booking.objects.filter(
            room=room,
            status='Confirmed',  # Only Confirmed bookings block availability
            check_in__lt=check_out_date_obj,
            check_out__gt=check_in_date_obj
        )
        
        if conflicting_bookings.exists():
            messages.error(request, 'Room is no longer available for the selected dates.')
            return redirect('booking_verify', room_id=room_id)
        
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            hotel=room.hotel,
            room=room,
            check_in=check_in_date_obj,
            check_out=check_out_date_obj,
            total_amount=total_amount,
            status='Pending'
        )
        
        # Clear booking preview from session
        if 'booking_preview' in request.session:
            del request.session['booking_preview']
        
        messages.success(request, 'Booking submitted successfully! Your booking is pending confirmation.')
        return redirect('booking_confirmed', booking_id=booking.id)
        
    except (ValueError, Exception) as e:
        messages.error(request, 'Invalid booking data. Please try again.')
        return redirect('booking_verify', room_id=room_id)


@login_required
def booking_verification(request):
    """Booking verification page (legacy - for backward compatibility)"""
    # Get booking preview from session
    booking_preview = request.session.get('booking_preview')
    if not booking_preview:
        messages.error(request, 'Booking session expired. Please try again.')
        return redirect('home')
    
    # Get room and hotel details
    try:
        room = get_object_or_404(Room, id=booking_preview['room_id'])
        hotel = room.hotel
    except (KeyError, Room.DoesNotExist):
        messages.error(request, 'Invalid booking data. Please try again.')
        return redirect('home')
    
    # Calculate nights for display
    from datetime import datetime
    check_in_date = datetime.fromisoformat(booking_preview['check_in_date']).date()
    check_out_date = datetime.fromisoformat(booking_preview['check_out_date']).date()
    nights = (check_out_date - check_in_date).days
    
    context = {
        'user': request.user,
        'hotel': hotel,
        'room': room,
        'booking_preview': booking_preview,
        'nights': nights,
    }
    return render(request, 'hotel/booking_verification.html', context)


@login_required
def confirm_booking(request):
    """Confirm and save booking"""
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('home')
    
    booking_preview = request.session.get('booking_preview')
    if not booking_preview:
        messages.error(request, 'Booking session expired. Please try again.')
        return redirect('home')
    
    try:
        room = get_object_or_404(Room, id=booking_preview['room_id'])
        
        # Convert string dates back to date objects
        from datetime import datetime
        check_in_date = datetime.fromisoformat(booking_preview['check_in_date']).date()
        check_out_date = datetime.fromisoformat(booking_preview['check_out_date']).date()
        
        # Double-check availability before creating booking
        conflicting_bookings = Booking.objects.filter(
            room=room,
            status__in=['Pending', 'Confirmed'],
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )
        
        if conflicting_bookings.exists():
            messages.error(request, 'Room is no longer available for the selected dates.')
            return redirect('room_detail', room_id=room.id)
        
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            hotel=room.hotel,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_amount=booking_preview['total_amount'],
            status='Pending'  # Start as Pending, admin can confirm
        )
        
        # Clear booking preview from session
        if 'booking_preview' in request.session:
            del request.session['booking_preview']
        
        messages.success(request, 'Booking submitted successfully! Your booking is pending confirmation.')
        return redirect('booking_confirmed', booking_id=booking.id)
        
    except (KeyError, ValueError, Room.DoesNotExist) as e:
        messages.error(request, 'Invalid booking data. Please try again.')
        return redirect('home')


@login_required
def booking_confirmed(request, booking_id):
    """Booking confirmed page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'user': request.user,
        'room': booking.room,
        'hotel': booking.hotel,
        'nights': None,  # Will be calculated in template
        'total_amount': booking.total_amount,
        'check_in': booking.check_in,
        'check_out': booking.check_out,
        'room_type': booking.room.get_room_type_display(),
        'hotel_name': booking.hotel.name,
        'room_number': booking.room.room_number,
        'price_per_night': booking.room.price_per_night,
        'city': booking.hotel.city,
        'user_email': request.user.email,
        'user_name': request.user.get_full_name() or request.user.username,
        'booking_status': booking.status,
        'created_at': booking.created_at,
        'booking_id': booking.id,
        'special_requests': 'No special requests specified',
        'guest_count': booking.room.capacity,
    }
    return render(request, 'hotel/booking_confirmed.html', context)


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def room_list(request):
    """Room listing page"""
    rooms = Room.objects.filter(availability=True).select_related('hotel')
    
    # Filter by hotel if provided
    hotel_id = request.GET.get('hotel')
    if hotel_id:
        rooms = rooms.filter(hotel_id=hotel_id)
    
    # Filter by room type if provided
    room_type = request.GET.get('room_type')
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    # Optimized: Use only() for filter data to load only needed fields
    room_types = Room.objects.values_list('room_type', flat=True).distinct()
    hotels = Hotel.objects.only('id', 'name')
    
    context = {
        'rooms': rooms,
        'room_types': room_types,
        'hotels': hotels,
    }
    return render(request, 'hotel/room_list.html', context)