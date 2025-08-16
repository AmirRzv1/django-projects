from django.urls import path
from .views import *

app_name = "post"
urlpatterns = [
    path("post/<int:post_id>/<slug:post_slug>/", PostDetailView.as_view(), name="post_detail"),
    path("post_delete/<int:post_id>/", PostDeleteView.as_view(), name="post_delete"),

]