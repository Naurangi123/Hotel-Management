from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    hotel_image = models.ImageField(upload_to='hotel_images/', default='hotel_images/default_image.jpg',null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.address}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)  # e.g., Single, Double, Suite
    price = models.DecimalField(max_digits=8, decimal_places=2)
    room_image = models.ImageField(upload_to='room_images/', default='room_images/default_image.jpg',null=True, blank=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateField()
    num_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
    
    def __str__(self):
        return f"Booking for {self.user} in {self.room}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20)  # Paid, Pending, Failed
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment for {self.booking}"

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.hotel.name} by {self.user.username}"
