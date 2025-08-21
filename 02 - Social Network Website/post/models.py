from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    # make relation to the User model so the post connect to one user
    # each user many post - each post belong to one user
    # OneToMany Relation
    # related_name -> we use it to have access in reverse relation in our models
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
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

    # self is the post we are seeing
    # with this we count the likes
    def like_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        # with True we understand that user already liked the post
        # with False its the otherwise
        user_like = user.uvotes.filter(post=self).exists()
        if user_like:
            return True
        else:
            False




class Comment(models.Model):
    # which user is commenting
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomments")
    # which post is getting a comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomments")
    # inner comment for reply - we need to connect the Comment model to itself
    # tip : not all the comments are reply, some of them are the main comment so
    # we need to create it empty first
    reply = models.ForeignKey("self", models.CASCADE, related_name="rcomments", blank=True, null=True)
    # the comment is reply or not
    is_reply = models.BooleanField(default=False)
    # the comment itself
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"

# create this model for counting likes for each post
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pvotes")

    def __str__(self):
        return f"{self.user} liked {self.post.slug}"

