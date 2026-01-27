from django.shortcuts import render
from django.views import View
from .forms import *

# Create your views here.
class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        pass
