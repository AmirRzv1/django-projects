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
                User.objects.create_user(username=data["username"], email=data["email"], password=data["password"])
                messages.success(request, "User created successfully.")
                return redirect("home:user_login")
                # return redirect(request, "accounts:user_login")
            except IntegrityError:
                form.add_error("username", "This username already exists.")
                messages.error(request, "User already exists !", "danger")

        return render(request, "accounts/register.html", {"form": form})

class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/login.html", {"form": form})

    def validate_username_or_email(self, data):
        if data.get("email"):
            return {"email": data["email"].lower()}
        else:
            return {"username": data["username"].lower()}

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            print(data["username"])
            # print(data["email"])
            # whether it is email or username
            result = self.validate_username_or_email(data)

            if result.get("username", None):
                user = authenticate(username=data["username"], password=data["password"])
                if user:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect("home:home")
                else:
                    messages.error(request, "Invalid Credential !!")
                    return redirect("home:home")


            else:
                real_user = User.objects.get(email=data["username"])
                user = authenticate(username=real_user.username, password=data["password"])
                if user:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect("home:home")
                else:
                    messages.error(request, "Invalid Credential !!")
                    return redirect("home:home")


        #     user_request_info = [data["username"], data["email"]]
        #     if "@" in user_request_info:
        #         user = authenticate(email=user_request_info[1], password=data["password"])
        #         if user:
        #             login(request, user)
        #             messages.success(request, "Logged in successfully!")
        #             return redirect("home:home")
        #         else:
        #             messages.error(request, "Invalid Credential !!")
        #     else:
        #         user = authenticate(username=user_request_info[0], password=data["password"])
        #         if user:
        #             login(request, user)
        #             messages.success(request, "Logged in successfully!")
        #             return redirect("home:home")
        #         else:
        #             messages.error(request, "Invalid Credential !!")
        #
        # return render(request, "accounts/login.html", {"form": form})

class UserLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "User logged out successfully !")
        return redirect("home:home")

