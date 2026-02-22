from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import *
import requests
import json


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

            try:
                response = requests.post(
                    "http://127.0.0.1:8001/accounts/login/",
                    json={"username": username, "password": password},
                    timeout=5
                )
                response.raise_for_status()  # raise exception for HTTP 4xx/5xx
                response_result = response.json()

            except requests.ConnectionError:
                messages.error(request, "Cannot reach authentication server. Try again later.")
                return render(request, "accounts/login.html", {"form": form})

            except requests.Timeout:
                messages.error(request, "Authentication server timed out. Try again later.")
                return render(request, "accounts/login.html", {"form": form})

            except requests.HTTPError:
                messages.error(request, f"Authentication failed: {response.status_code}")
                return render(request, "accounts/login.html", {"form": form})

            except json.JSONDecodeError:
                messages.error(request, "Invalid response from authentication server.")
                return render(request, "accounts/login.html", {"form": form})

            if response_result.get("success"):
                request.session["user_id"] = response_result["user_id"]
                request.session["username"] = response_result["username"]
                request.session["user_is_authenticated"] = True
                messages.success(request, "User successfully logged in.")
                return redirect("core:home")
            else:
                messages.error(request, response_result.get("error", "Invalid credentials"))
                return render(request, "accounts/login.html", {"form": form})

class UserLogoutView(View):
    def post(self, request):
        user_id = request.session.get("user_id")
        print("user_id = ", user_id)
        if not user_id:
            messages.error(request, "You are not logged in.")
            return redirect("core:home")

        response = requests.post("http://127.0.0.1:8001/accounts/logout/",
                                 json={"user_id": user_id},
                                 timeout=5
                                 )
        print("respnse = ", response)
        final_response = response.json()
        print("final_result = ", final_response)
        if final_response.get("success"):
            request.session.pop("user_id", None)
            request.session.pop("username", None)
            request.session.pop("user_is_authenticated", None)
            messages.success(request, "User successfully logged out.")
            return redirect("core:home")

class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register.html", {"form": form})









