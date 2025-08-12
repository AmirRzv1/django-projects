from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
class UserRegisterView(View):
    # we use this kind of naming as a class variable so we stop repeating our self
    form_class = UserRegisterForm
    # we use template name a lot so we set this as a class variable
    template_name = "account/register.html"

    # with get we show the form to user, in order to fill the information
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # with post we collect the data from our user and start validating
    def post(self, request):
        # we need to pass the request.POST to our form to use its functionality
        form = self.form_class(request.POST)
        if form.is_valid():
            # data which is valid and we receive it from our form
            cd = form.cleaned_data
            username = cd["username"]
            email = cd["email"]
            password = cd["password1"]
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "You Registered Successfully !", "success")
            # first namespace then the url name
            return redirect("home:home")
        # if the input vars from user is invalid so we show the page again with the right error message
        return render(request, self.template_name, {"form": form})
