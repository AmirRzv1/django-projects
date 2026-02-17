from asyncio import timeout

from django.shortcuts import render, redirect
from django.views import View
from .forms import *
import requests


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
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = request.post("http://127.0.0.1:8001/accounts/login/",
                                json={"username": username, "password": password},
                                timeout=5)
        response_result = response.json()
        if response_result.get("success"):
            return redirect("home")










