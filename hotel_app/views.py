from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Room,Hotel,Booking
from .forms import HotelForm,RoomForm

# Create your views here.
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel=Hotel.objects.prefetch_related('rooms').get(id=hotel_id)
    rooms=hotel.rooms.all()
    return render(request, 'hotel/hotel_detail.html', {'hotel': hotel,'rooms':rooms})

def available_rooms(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    available_rooms = Room.objects.filter(hotel=hotel, available=True)
    return render(request, 'hotel/available_rooms.html', {'hotel': hotel, 'rooms': available_rooms})

def add_room(request, hotel_id):
    hotel=get_object_or_404(Hotel,id=hotel_id)
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.hotel=hotel
            room.save()
            messages.success("Room Added Successfully!")
            return redirect('available_rooms', hotel_id=hotel.id)
    else:
        form=RoomForm()
        return render(request, 'hotel/add_room.html', {'hotel': hotel,'form':form})

def hotel_create(request):
    if request.method=='POST':
        form=HotelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success("Hotel Added Successfully!")
            return redirect('hotel_list')
    else:
        form=HotelForm()
    return render(request, 'hotel/add_hotel.html', {'form': form})

def hotel_update(request, hotel_id):
    hotel = get_object_or_404(Hotel,id=hotel_id)
    if request.method == 'POST':
        form=HotelForm(request.POST,instance=hotel)
        if form.is_valid():
            form.save()
            return redirect("hoteil_detail",hotel_id=hotel.id)
    else:
        form=HotelForm(instance=hotel)
    return render(request, 'hotel/edit_hotel.html', {'hotel': hotel,'form':form})

def room_booking(request,hotel_id,room_id):
    hotel = get_object_or_404(Hotel,id=hotel_id)
    room = get_object_or_404(Room,id=room_id)
    if room.available:
        if request.method == 'POST':
            booking = Booking(user=request.user, room=room, check_in=request.POST['check_in'])
            booking.save()
            room.available = False
            room.save()
            messages.success("request,Booking Successful!")
            return render(request, 'hotel/booking_success.html')
        else:
            return render(request, 'hotel/book_room.html', {'hotel': hotel, 'room': room})
    else:
        messages.error("Sorry, this room is not available.")
        return render(request, 'hotel/available_rooms.html', {'hotel': hotel, 'rooms': hotel.rooms.filter(available=True)})

def room_check_in(request,room_id):
    room = get_object_or_404(Room,id=room_id)
    return render(request, 'hotel/check_in.html', {'room': room})

def room_check_out(request,room_id):
    room=get_object_or_404(Room,id=room_id)
    if request.method == 'POST':
        booking=Booking.objects.get(room=room)
        booking.status='Confirmed'
        booking.check_out=request.POST['check_out']
        booking.save()
        room.available=True
        room.save()
        messages.success(request,'Check Out Successfully!')
        return redirect('booking_history', user_id=request.user.id)
    else:
        return render(request, 'hotel/check_out.html', {'room':room})
    
def booking_history(request, user_id):
    booking=Booking.objects.filter(user=user_id)
    return render(request,'hotel/booking_history.html',{'booking':booking})
