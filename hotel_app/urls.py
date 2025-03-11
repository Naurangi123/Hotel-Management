from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('hotel/create/', views.hotel_create, name='hotel_create'),
    path('hotel/<int:hotel_id>/update/', views.hotel_update, name='hotel_update'),
    
    path('hotel/<int:hotel_id>/rooms/', views.available_rooms, name='available_rooms'),
    path('hotel/<int:hotel_id>/room/add/', views.add_room, name='add_room'),
    
    path('hotel/<int:hotel_id>/room/<int:room_id>/book/', views.room_booking, name='room_booking'),
    path('booked-rooms/', views.booked_rooms, name='booked_rooms'),
    path('room/<int:room_id>/checkout/', views.check_out_room, name='check_out_room'),
    
    path('booking-history/<int:user_id>/', views.booking_history, name='booking_history'),
]
