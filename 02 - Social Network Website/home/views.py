from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # This kind of mapping for temp files is because we made an inner
    # folder named templates inside our app and it has a html file
    # and we want to access to it so first the name of the folder in templates
    # then the exact name of our template
    return render(request, "home/index")