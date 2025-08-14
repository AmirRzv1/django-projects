from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    # make relation to the User model so the post connect to one user
    # each user many post - each post belong to one user
    # OneToMany Relation
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    # this is a string for reading urls better
    slug = models.SlugField()
    # first created - only once
    created = models.DateTimeField(auto_now_add=True)
    # each updates for post - multiple time
    updated = models.DateTimeField(auto_now=True)

    # after adding this part there is no need to migrate
    # because its a action - after changing fields we need it
    def __str__(self):
        return f"{self.user}: {self.slug}"