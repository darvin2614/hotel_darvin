from django import forms
from .models import Hotel, Room

class HotelForm(forms.ModelForm):
    """Form for creating and editing hotels"""
    class Meta:
        model = Hotel
        fields = [
            'name', 'city', 'address', 'description', 
            'hotel_image_url', 'rating'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hotel name'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full address'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter hotel description'
            }),
            'hotel_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL (optional)'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'step': 0.1,
                'placeholder': '1.0 - 5.0'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel_image_url'].required = False
        self.fields['rating'].initial = 4.0

class RoomForm(forms.ModelForm):
    """Form for creating and editing rooms"""
    class Meta:
        model = Room
        fields = [
            'hotel', 'room_number', 'room_type', 'price_per_night',
            'capacity', 'availability', 'room_image_url', 'description'
        ]
        widgets = {
            'hotel': forms.Select(attrs={
                'class': 'form-control'
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 101, A201'
            }),
            'room_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price_per_night': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01,
                'placeholder': '0.00'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Number of guests'
            }),
            'availability': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'room_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Room description (optional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_image_url'].required = False
        self.fields['description'].required = False
        self.fields['availability'].initial = True
