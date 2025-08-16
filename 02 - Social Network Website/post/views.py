from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, "post/detail.html", {"post": post})

    def post(self, request):
        pass

class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        user = request.user.id
        owner = Post.objects.get(pk=post_id)
        if user == owner.user.id:
            Post.objects.remove(id=post_id)
            messages.success(request, "Post Deleted Successfully !", "success")
            return redirect("home:home")
        messages.warning(request, "You are not the owner of the post !")
        return redirect("home:home")

