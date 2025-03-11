from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from .models import Room, Hotel, Booking
from .forms import HotelForm, RoomForm, BookRoomForm

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel.objects.prefetch_related('rooms'), id=hotel_id)
    rooms = hotel.rooms.all()
    return render(request, 'hotel/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

def available_rooms(request, hotel_id=None):
    hotel = get_object_or_404(Hotel, id=hotel_id) if hotel_id else None
    rooms = Room.objects.filter(hotel=hotel) if hotel else Room.objects.all()
    booked_rooms = Booking.objects.values_list('room_id', flat=True)
    available_rooms = rooms.exclude(id__in=booked_rooms)
    return render(request, 'hotel/available_rooms.html', {'hotel': hotel, 'rooms': available_rooms})

def add_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            messages.success(request, "Room Added Successfully!")
            return redirect('available_rooms', hotel_id=hotel.id)
    else:
        form = RoomForm()
    return render(request, 'hotel/add_room.html', {'hotel': hotel, 'form': form})

def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel Added Successfully!")
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'hotel/add_hotel.html', {'form': form})

def hotel_update(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect("hotel_detail", hotel_id=hotel.id)
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'hotel/edit_hotel.html', {'hotel': hotel, 'form': form})

def room_booking(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(Room, id=room_id)
    if Booking.objects.filter(room=room).exists():
        messages.error(request, "Sorry, this room is already booked.")
        return redirect('available_rooms', hotel_id=hotel.id)
    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.check_in = timezone.now()
            booking.status = 'Confirmed'
            booking.save()
            messages.success(request, "Booking Successful!")
            return redirect('booked_rooms')
    else:
        form = BookRoomForm()
    return render(request, 'hotel/book_room.html', {'hotel': hotel, 'room': room, 'form': form})

def booked_rooms(request,room_id):
    rooms = Booking.objects.select_related('room').get(id=room_id)
    return render(request, 'hotel/booked_room.html', {'rooms': rooms})

def check_out_room(request, room_id):
    booking = get_object_or_404(Booking, room_id=room_id, status='Confirmed')
    booking.status = 'Checked Out'
    booking.check_out_time = timezone.now()
    booking.total_charges = calculate_total_charges(booking)
    booking.room.available = True
    booking.room.save()
    booking.save()
    messages.success(request, "Checked out successfully!")
    return redirect('booked_rooms')

def booking_history(request, user_id):
    bookings = Booking.objects.filter(user_id=user_id)
    return render(request, 'hotel/booking_history.html', {'bookings': bookings})

def calculate_total_charges(booking):
    if not booking.check_in or not booking.check_out_time:
        return 0
    nights_stayed = max((booking.check_out_time - booking.check_in).days, 1)
    return nights_stayed * booking.room.price
