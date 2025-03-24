from django.shortcuts import render,redirect
from .models import UserProfile
from django.contrib.auth import login ,authenticate,logout
from django.contrib.auth.decorators import login_required
from.forms import UserProfileForm,CustomUserCreationForm,LoginForm
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! You are now able to log in.')
            return redirect('login_view')
    else:
        form = CustomUserCreationForm()
    return render(request,'userapp/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('profile_view')
            else:
                messages.error(request, "Invalid login credentials")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = LoginForm()

    return render(request, 'userapp/login.html', {'form': form})
    
@login_required
def profile_view(request):
    return render(request, 'userapp/profile.html',{'user':request.user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'userapp/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login_view')