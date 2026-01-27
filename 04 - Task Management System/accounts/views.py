from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.db import IntegrityError

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
            except IntegrityError:
                form.add_error('username', 'Username already exists')
                return render(request, 'accounts/register.html', {'form': form})

            return render(request, "core/landing.html")


