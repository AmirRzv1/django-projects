from django.urls import path
from .views import *

app_name = "review"
urlpatterns = [
    path("create/", ReviewCreateView.as_view(), name="review_create")
]