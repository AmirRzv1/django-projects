from .models import Profile, User
from django.db.models.signals import post_save


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])

post_save.connect(receiver=create_profile, sender=User)