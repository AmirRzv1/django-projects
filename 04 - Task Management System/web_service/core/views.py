from django.shortcuts import render
from django.views import View
from .forms import *


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, "landing.html")

class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        pass

