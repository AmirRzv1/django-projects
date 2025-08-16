from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm

# Create your views here.
class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, "post/detail.html", {"post": post})

    def post(self, request):
        pass

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        user = request.user.id
        post = Post.objects.get(pk=post_id)
        if user == post.user.id:
            post.delete()
            messages.success(request, "Post Deleted Successfully !", "success")
            return redirect("home:home")
        messages.warning(request, "You are not the owner of the post !")
        return redirect("home:home")

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    # dispatch here checks that the user which is trying to update
    # is the real owner or not.
    # if he is no the owner shows an error.
    def dispatch(self, request, *args, **kwargs):
        user = request.user.id
        post = Post.objects.get(pk=kwargs["post_id"])
        if not user == post.user.id:
            messages.warning(request, "You are not the owner ! ", "danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        pass

    def post(self, request, post_id):
        pass