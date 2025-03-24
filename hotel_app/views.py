from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg
from datetime import datetime
from .models import Room, Hotel, Booking
from .forms import HotelForm, RoomForm, BookRoomForm


def index(request):
    return render(request, 'hotel/home.html')

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

def hotel_rooms(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        hotels = Hotel.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
        return render(request, 'hotel/hotel_list.html', {'hotels': hotels})
    else:
        rooms=Room.objects.select_related('hotel').all()
        return render(request, 'hotel/hotel_rooms.html',{'rooms':rooms})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel.objects.prefetch_related('rooms'), id=hotel_id)
    rooms = hotel.rooms.all()
    
    average_rating = hotel.rating
    
    full_stars = int(average_rating)
    has_half_star = (average_rating % 1) >= 0.5  
    full_star_range = range(full_stars)
    empty_star_range = range(full_stars, 5)
    context= {
        'hotel': hotel,
        'rooms': rooms,
        'full_star_range': full_star_range,
        'has_half_star': has_half_star,
        'empty_star_range': empty_star_range,
        }
    return render(request, 'hotel/hotel_detail.html',context)

def available_rooms(request, hotel_id=None):
    hotel = get_object_or_404(Hotel, id=hotel_id) if hotel_id else None
    rooms = Room.objects.filter(hotel=hotel) if hotel else Room.objects.all()
    booked_rooms = Booking.objects.values_list('room_id', flat=True)
    available_rooms = rooms.exclude(id__in=booked_rooms)
    return render(request, 'hotel/available_rooms.html', {'hotel': hotel, 'rooms': available_rooms})

login_required
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


login_required
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


login_required
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

login_required
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
            booking.check_in = datetime.now()
            booking.status = 'Confirmed'
            booking.save()
            messages.success(request, "Booking Successful!")
            return redirect('booked_rooms')
    else:
        form = BookRoomForm() 
    return render(request, 'hotel/book_room.html', {'hotel': hotel, 'room': room, 'form': form})


def booked_rooms(request):
    rooms = Booking.objects.select_related('room').all()
    return render(request, 'hotel/booked_room.html', {'rooms': rooms})

login_required
def check_out_room(request, room_id):
    try:
        booking = Booking.objects.get(room_id=room_id, status='Confirmed')
        booking.status = 'Checked Out'
        booking.check_out_time = datetime.now().strftime("%Y-%m-%d")
        booking.total_charges = calculate_total_charges(booking)
        booking.room.available = True
        booking.room.save()
        booking.save()
        messages.success(request, "Checked out successfully!")
    except Booking.DoesNotExist:
        messages.error(request, "No active booking found for this room.")
    return redirect('booked_rooms')


def booking_history(request, user_id):
    bookings = Booking.objects.filter(user_id=user_id)
    return render(request, 'hotel/booking_history.html', {'bookings': bookings})

from django.utils.timezone import localtime

def calculate_total_charges(booking):
    if not booking.check_in or not booking.check_out:
        return 0

    check_in = localtime(booking.check_in)
    check_out = localtime(booking.check_out)

    stay_duration = check_out - check_in
    nights_stayed = max(stay_duration.total_seconds() / (24 * 3600), 1)

    return round(nights_stayed * booking.room.price, 2)

