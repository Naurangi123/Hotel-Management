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
        model = Booking
        fields = ['check_in', 'num_guests', 'special_requests']
        exclude = ['check_out',]

    check_in = forms.DateField(widget=forms.SelectDateWidget(), label='Check-in Date')
    num_guests = forms.IntegerField(min_value=1, max_value=10, label='Number of Guests')
    special_requests = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Any special requests? (Optional)'}), required=False)
