from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.contrib.auth import views as auth_views

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

    # check that if the user is sending the username or email
    # based on that we return the related information
    def validate_username_or_email(self, data):
        login_info = data.get("username")
        if login_info and "@" in login_info:
            return {"email": login_info.lower()}
        else:
            return {"username": login_info.lower()}


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data
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

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "User logged out successfully !")
        return redirect("home:home")

class CostumePasswordResetView(auth_views.PasswordResetView):
    pass

class CostumePasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass

class CostumePasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    pass

class CostumePasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass

