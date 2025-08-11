from django.shortcuts import render
from django.views import View

# Camel Case naming for classes
class HomeView(View):
    def get(self, request):
        # This kind of mapping for temp files is because we made an inner
        # folder named templates inside our app and it has a html file
        # and we want to access to it so first the name of the folder in templates
        # then the exact name of our template
        # the home i mentioned here is not my app name its the name of my
        # folder inside the templates folder in home app
        return render(request, "home/index.html")
