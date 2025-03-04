from . import views
from django.urls import path


urlpatterns = [
    path('', views.hotel_list, name='home'),
    path('hotel/<int:hotel_id>/',views.hotel_detail,name='hotel_detail'),
]