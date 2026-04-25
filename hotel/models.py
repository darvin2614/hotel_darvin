from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    hotel_image_url = models.URLField(max_length=500, default='https://picsum.photos/400/300')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price_range = models.CharField(max_length=50)  # e.g., "$$", "$$$", "$$$$"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}"

    @property
    def average_room_price(self):
        # Optimized: Use aggregate instead of loading all rooms
        from django.db.models import Avg
        result = self.rooms.aggregate(avg_price=Avg('price_per_night'))
        return result['avg_price'] or 0


class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    room_image_url = models.URLField(max_length=500, default='https://picsum.photos/400/300')
    description = models.TextField()
    room_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type} ({self.room_number})"

    def is_available(self, check_in, check_out):
        """Check if room is available for given dates"""
        # Optimized: Use single query with proper field names
        bookings = self.bookings.filter(
            status__in=['Pending', 'Confirmed'],
            check_in__lt=check_out,  # existing check-in before new check-out
            check_out__gt=check_in   # existing check-out after new check-in
        )
        return not bookings.exists()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} ({self.check_in} to {self.check_out})"

    def calculate_total_amount(self):
        """Calculate total amount based on number of nights and room price"""
        nights = (self.check_out - self.check_in).days
        return nights * self.room.price_per_night
    
    @property
    def nights(self):
        """Calculate number of nights"""
        return (self.check_out - self.check_in).days

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    @property
    def can_cancel(self):
        """Check if booking can be cancelled"""
        return self.status in ['Pending', 'Confirmed'] and self.check_in > timezone.now().date()