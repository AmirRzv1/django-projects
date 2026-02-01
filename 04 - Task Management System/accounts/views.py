from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import *

# Create your views here.
class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.create_user(username=data["username"], password=data["password"])
                messages.success(request, "User created successfully.")
                return redirect("home:home")
                # return redirect(request, "accounts:user_login")
            except IntegrityError:
                form.add_error("username", "This username already exists.")
                messages.error(request, "User already exists !", "danger")

        return render(request, "accounts/register.html", {"form": form})

class UserLoginView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home:home")
            else:
                messages.error(request, "Invalid Credential !!")
        return render(request, "accounts/login.html", {"form": form})

class UserLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "User logged out successfully !")
        return redirect("home:home")

