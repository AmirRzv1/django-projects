from django.db import models

# Create your models here.
class Task(models.Model):
    # List of tuples and 2 string, first for DB
    # and second for human readable.
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ('soft_delete', 'Soft Delete'),
    ]

    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=15, default="ongoing", choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.IntegerField()

    def __str__(self):
        return self.title + "-" + self.status