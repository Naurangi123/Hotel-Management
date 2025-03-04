from django import forms
from .models import Hotel, Room


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description', 'rating']
        
class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields=['room_type', 'price', 'available']
        
    price=forms.DecimalField(max_digits=8,decimal_places=2,widget=forms.NumberInput(attrs={'step':'0.01'}))