from django.urls import path
from .views import *

app_name = "review"
urlpatterns = [
    path("create-movie/", MovieCreateView.as_view(), name="movie_create"),
    path("all-movies/", MovieCreateView.as_view(), name="movie_all"),
    path("create/", ReviewCreateView.as_view(), name="review_create")
]