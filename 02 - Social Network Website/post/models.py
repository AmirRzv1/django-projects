from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

    # after defining our fields we need to define Meta
    # for sorting and ordering option
    # tip : this is globally for ordering
    class Meta:
        # this will order based on the field we gave
        ordering = ["-created"]

    # after adding this part there is no need to migrate
    # because its a action - after changing fields we need it
    def __str__(self):
        return f"{self.user}: {self.slug}"

    # we use this function to define the url for our post so when we want
    # to call it and use it it is easier and we just say the function name
    # in out templates
    def get_absolute_url(self):
        return reverse("post:post_detail", args=[self.id, self.slug])