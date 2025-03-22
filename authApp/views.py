from django.shortcuts import render
from .models import UserProfile

# Create your views here.

def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})