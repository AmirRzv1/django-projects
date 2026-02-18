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
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username")
            password = data.get("password")

            response = requests.post("http://127.0.0.1:8001/accounts/login/",
                                    json={"username": username, "password": password},
                                    timeout=5)
            print(response.status_code)
            print(response.text)
            response_result = response.json()
            print("response result : ", response_result)
            if response_result.get("success"):
                return redirect("core:home")










