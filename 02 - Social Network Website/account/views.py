from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
class RegisterView(View):
    # with get we show the form to user, in order to fill the information
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "account/register.html", {"form": form})

    # with post we collect the data from our user and start validating
    def post(self, request):
        # we need to pass the request.POST to our form to use its functionality
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # data which is valid and we receive it from our form
            cd = form.cleaned_data
            username = cd["username"]
            email = cd["email"]
            password = cd["password"]
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "You Registered Successfully !", "success")
            # first namespace then the url name
            return redirect("home:home")
