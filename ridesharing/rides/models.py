from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    RIDER = 'rider'
    DRIVER = 'driver'

    USER_TYPE_CHOICES = [
        (RIDER, 'Rider'),
        (DRIVER, 'Driver'),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=RIDER,
    )

    def __str__(self):
        return self.username


from django.db import models
from django.conf import settings

class Ride(models.Model):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rides_as_rider'
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rides_as_driver'
    )
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status} from {self.pickup_location} to {self.dropoff_location}"
