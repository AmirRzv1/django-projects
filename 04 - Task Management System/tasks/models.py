from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    # List of tuples and 2 string, first for DB
    # and second for human readable.
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("done", "Done")
    ]

    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, default="on going", choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")