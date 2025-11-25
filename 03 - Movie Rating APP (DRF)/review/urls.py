from django.urls import path
from views import *

urlpatterns = [
    path("create/", ReviewCreateView.as_view(), name="review_create")
]