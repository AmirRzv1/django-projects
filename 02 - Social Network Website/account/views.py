from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class UserRegisterView(View):
    # we use this kind of naming as a class variable so we stop repeating our self
    form_class = UserRegisterForm
    # we use template name a lot so we set this as a class variable
    template_name = "account/register.html"

    # this mehod runs before others and take the control first
    # in this case i want to check that if the user already logged in
    # so i dont show him the register page again
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            messages.warning(request, "You already logged in", "warning")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)


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

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            messages.warning(request, "You already logged in", "warning")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd["username"]
            password = cd["password"]
            # here we authenticate our user that its pass and username matches
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # here it login our user based on the user we gave to it
                login(request, user)
                messages.success(request, f"User '{user}' logged in successfully", "success")
                return redirect("home:home")
            messages.error(request, "Username or Password is wrong", "warning")
        return render(request, self.template_name, {"form": form})

# this is for user log out we just need to
# call the function and pass the request to it
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        logout(request)
        messages.success(request, f"User '{username}' Logout Successfully!", "success")
        return redirect("home:home")

# this LoginRequiredMixin only let the logged in users to see the profile
class UserProfileView(LoginRequiredMixin, View):
    # this user_id is the id which comes from the url and we get it here
    def get(self, request, user_id):
        # here we get the related user data and send it to the related template file
        user = User.objects.get(id=user_id)
        return render(request, "account/profile.html", {"user": user})


