from django.contrib import admin
from .models import Post, Comment

# creating the costume admin here
# way 1 -> we also can register the setting with the decorator
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # it tells django which fields we want to show in admin panel
    list_display = ["user", "slug", "updated", "created"]
    # it show a bar in admin panel and let us to search in slug
    search_fields = ["slug"]
    # to filter each field we want, here base on date for updated
    list_filter = ["updated"]
    # how to fill slug based on other fields
    prepopulated_fields = {"slug": ["body"]}
    # let us to see the whole users and select the one we want
    raw_id_fields = ["user"]

# way 2 --> we can register the model and the setting for our admin panel like this
# after defining the class and its feature add the class name here
# admin.site.register(Post, PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "is_reply", "created"]
    raw_id_fields = ["user", "post", "reply"]