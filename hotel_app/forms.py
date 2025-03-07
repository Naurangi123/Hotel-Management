from django import forms
from .models import Hotel, Room,Booking


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description', 'rating']
        
class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields=['room_type', 'price', 'available']
        
    price=forms.DecimalField(max_digits=8,decimal_places=2,widget=forms.NumberInput(attrs={'step':'0.01'}))
    
class BookRoomForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=['user','room','check_in','check_out','status']
        
class BookRoomForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=['user','room','check_in','check_out','status']