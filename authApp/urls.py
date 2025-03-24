from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile_view'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('edit-profile/', views.update_profile, name='edit_profile'),
]
