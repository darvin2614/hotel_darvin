# Hotel Management System

A full-stack Hotel Management System built with Django and SQLite, featuring hotel bookings, user authentication, and admin dashboard.

## Features

- **Hotel Management**: Add, edit, and manage hotels in different cities
- **Room Management**: Manage different room types with pricing and availability
- **Booking System**: Users can book rooms with date selection and availability checking
- **User Authentication**: Registration, login, and logout functionality
- **Admin Dashboard**: Comprehensive admin interface for managing all aspects
- **Responsive Design**: Modern UI using Bootstrap 5
- **Search & Filter**: Search hotels by city or name, filter rooms by type

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite
- **Authentication**: Django's built-in authentication system
- **Admin Panel**: Django Admin

## Project Structure

```
hotel_management/
├── hotel_management/          # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── hotel/                     # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── tests.py
│   └── management/
│       └── commands/
│           └── create_dummy_data.py
├── templates/
│   ├── base.html
│   └── hotel/
│       ├── home.html
│       ├── hotel_list.html
│       ├── hotel_detail.html
│       ├── room_list.html
│       ├── room_detail.html
│       ├── booking.html
│       ├── my_bookings.html
│       ├── login.html
│       ├── signup.html
│       └── admin_dashboard.html
├── static/
│   └── css/
│       └── style.css
├── manage.py
└── requirements.txt
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone and Setup

1. Navigate to the project directory:
   ```bash
   cd pt5
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Database Setup

1. Create database migrations:
   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations:
   ```bash
   python manage.py migrate
   ```

### Step 3: Create Superuser

1. Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```
   
   Follow the prompts to create your admin account.

### Step 4: Generate Dummy Data

1. Create sample hotels and rooms:
   ```bash
   python manage.py create_dummy_data
   ```

This will create:
- 8 hotels across Chennai, Mumbai, Bangalore, and Delhi
- Multiple rooms for each hotel (Single, Double, Deluxe, Suite)
- Realistic pricing based on hotel ratings and locations

### Step 5: Run the Development Server

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to:
   - **Home Page**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/
   - **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/

## Usage Guide

### For Regular Users

1. **Browse Hotels**: Visit the home page or click "Hotels" in the navigation
2. **Search Hotels**: Use the search form to filter by city or hotel name
3. **View Rooms**: Click on a hotel to see available rooms
4. **Book a Room**: 
   - Click "Book Now" on any available room
   - Select check-in and check-out dates
   - Review the booking summary
   - Confirm your booking
5. **Manage Bookings**: View and cancel your bookings from "My Bookings"

### For Admin Users

1. **Access Admin Dashboard**: Click "Admin Dashboard" (requires superuser privileges)
2. **View Statistics**: Monitor total hotels, rooms, bookings, and users
3. **Manage Bookings**: Confirm or cancel pending bookings
4. **Django Admin**: Access full admin functionality at /admin/ for:
   - Adding/editing hotels
   - Adding/editing rooms
   - Managing users
   - Full CRUD operations

## Features in Detail

### Hotel Module
- Multiple hotels across major Indian cities
- Hotel information: name, city, address, description, rating, price range
- Hotel images using Unsplash URLs
- Search and filter functionality

### Room Module
- Four room types: Single, Double, Deluxe, Suite
- Room details: price per night, capacity, availability
- Room images and descriptions
- Availability checking during booking

### Booking Module
- Date selection with validation
- Automatic price calculation
- Availability checking to prevent double bookings
- Booking status management (Pending, Confirmed, Cancelled, Completed)
- User booking history

### User Authentication
- User registration with email validation
- Secure login/logout functionality
- User-specific booking management

### Admin Dashboard
- Real-time statistics
- Recent bookings overview
- Quick booking management actions
- Links to Django admin for advanced management

## Sample Data

The dummy data includes hotels in:

- **Mumbai**: Taj Mahal Palace, Marriott Suites Pune
- **Bangalore**: The Leela Palace, Vivanta Bengaluru
- **Chennai**: ITC Grand Chola, Radisson Blu Temple Bay
- **Delhi**: The Imperial, The Oberoi Gurgaon

Each hotel has multiple rooms with realistic pricing based on:
- Hotel rating
- Room type
- City location

## Troubleshooting

### Common Issues

1. **Port Already in Use**: Change the port using `python manage.py runserver 8001`
2. **Migration Issues**: Delete `db.sqlite3` and re-run migrations
3. **Static Files Not Loading**: Run `python manage.py collectstatic`
4. **Images Not Loading**: Check internet connection (images are from Unsplash URLs)

### Development Tips

1. Use Django Debug Toolbar for debugging
2. Enable DEBUG=True in settings.py for development
3. Use Django shell for testing: `python manage.py shell`
4. Check Django admin at /admin/ for data management

## Contributing

This is a demo project for educational purposes. Feel free to extend it with:

- Payment integration
- Email notifications
- Advanced search filters
- Reviews and ratings system
- Multi-language support

## License

This project is for educational purposes only.
