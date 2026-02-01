from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages

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

class UserLoginView():
    pass


