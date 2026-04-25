from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hotel, Room, Booking
from datetime import date, timedelta


class HotelSearchForm(forms.Form):
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search by city...'
    }))
    hotel_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search by hotel name...'
    }))


class BookingForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
    }))
    check_out = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
    }))

    def __init__(self, room, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        
        # Calculate dates only when form is instantiated, not at import time
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        self.fields['check_in'].widget.attrs.update({
            'min': today.strftime('%Y-%m-%d')
        })
        self.fields['check_out'].widget.attrs.update({
            'min': tomorrow.strftime('%Y-%m-%d')
        })

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            # Validate dates
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")
            
            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be after check-in date.")
            
            # Note: Room availability is handled in the view, not here
            # This allows for better error handling and debugging

        return cleaned_data

    def calculate_total_amount(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')
        if check_in and check_out:
            nights = (check_out - check_in).days
            return nights * self.room.price_per_night
        return 0


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'city', 'address', 'description', 'rating', 'price_range', 'hotel_image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5, 'step': 0.1}),
            'price_range': forms.Select(attrs={'class': 'form-control'}),
            'hotel_image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user