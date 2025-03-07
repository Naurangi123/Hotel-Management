from . import views
from django.urls import path


urlpatterns = [
    path('', views.hotel_list, name='home'),
    path('hotel/<int:hotel_id>/',views.hotel_detail,name='hotel_detail'),
    path('hotel/<int:hotel_id>/add_room',views.add_room,name='add_room'),
    path('hotel/<int:hotel_id>/available_rooms',views.available_rooms,name='available_rooms'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/',views.room_booking,name='room_booking'),
    path('hotel/<int:room_id>/room_check_out/',views.room_check_out,name="room_check_out"),
    path('hotel/booked_room/',views.booked_room,name='booked_room'),
    path('rooms/available/', views.available_rooms, name='available_rooms'),
    path('rooms/available/<int:hotel_id>/', views.available_rooms, name='available_rooms_by_hotel'),
]