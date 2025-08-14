from django.shortcuts import render
from django.views import View
from .models import Post

# Create your views here.
class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, "post/detail.html", {"post": post})

    def post(self, request):
        pass