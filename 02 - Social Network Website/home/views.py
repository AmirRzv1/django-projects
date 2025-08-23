from django.shortcuts import render
from django.views import View
from post.models import Post
from .forms import *

# Camel Case naming for classes
class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        # new code with ordering
        # this is like all and takes all the data but we cant have order
        # by passing the field to be ordered
        # for reverse ordering we can add a hyphen so it will be ordered reverse
        # tip : this type of ordering only works on this method and just here
        # if we want the whole model to be ordered we need to use Meta in models
        # posts = Post.objects.order_by("-created")

        # old code
        posts = Post.objects.all()

        # we use field lookups to search in our db to find the data we want
        # syntax = field__field lookups
        if request.GET.get("search"):
            posts = posts.filter(body__contains = request.GET["search"])

        # This kind of mapping for temp files is because we made an inner
        # folder named templates inside our app and it has a html file
        # and we want to access to it so first the name of the folder in templates
        # then the exact name of our template
        # the home i mentioned here is not my app name its the name of my
        # folder inside the templates folder in home app
        return render(request, "home/index.html", {"posts": posts, "form": self.form_class})

