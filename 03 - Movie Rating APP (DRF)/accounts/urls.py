from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path("create/", AccountCreateView.as_view(), name="create_account"),
    path("all/", AccountCreateView.as_view(), name="all_accounts"),
]