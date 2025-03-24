from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,AuthenticationForm
from .models import UserProfile

class UserProfileForm(UserChangeForm):
    class Meta:
        model=UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'bio', 'profile_picture']
        
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
   class Meta:
       model=UserProfile
       fields = ['username', 'password']