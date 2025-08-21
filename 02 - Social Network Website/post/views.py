from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import *
from django.utils.text import slugify
from .forms import CommentCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    # we want to use post several times so we add it here
    def setup(self, request, *args, **kwargs):
        self.post_isntance = get_object_or_404(Post, pk=kwargs["post_id"], slug=kwargs["post_slug"])
        return super().setup(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        # we use get_object_or_404 in order to show the user 404 error when trying
        # to fetch something which is not present in our database instead of server error 500
        # old way of getting the data
        # post = Post.objects.get(pk=post_id, slug=post_slug)
        # main comments with relate_name
        comments = self.post_isntance.pcomments.filter(is_reply=False)
        return render(request, "post/detail.html", {"post": self.post_isntance, "comments": comments,
                                                    "form": self.form_class, "reply_form": self.form_class_reply})

    # this will limit the access to logged-in user only
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # the only thing we will save is body, but we want more data so we use commit
            # equal False to extract and send the data manually
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_isntance
            new_comment.save()
            messages.success(request, "Comment submitted successfully !", "success")
            return redirect("post:post_detail", self.post_isntance.id, self.post_isntance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        user = request.user.id
        post = get_object_or_404(Post, pk=post_id)
        if user == post.user.id:
            post.delete()
            messages.success(request, "Post Deleted Successfully !", "success")
            return redirect("home:home")
        messages.warning(request, "You are not the owner of the post !")
        return redirect("home:home")

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    # in the setup we write a code that take th related record from our database
    # so we use it in other methods that we want
    # with this we only hit db once
    def setup(self, request, *args, **kwargs):
        # we save it in self so it will be reachable
        self.post_isntance = get_object_or_404(Post, pk=kwargs["post_id"])
        # we must call the super class
        return super().setup(request, *args, **kwargs)


    # dispatch here checks that the user which is trying to update
    # is the real owner or not.
    # if he is no the owner shows an error.
    def dispatch(self, request, *args, **kwargs):
        user = request.user.id
        post = self.post_isntance
        if not user == post.user.id:
            messages.warning(request, "You are not the owner ! ", "danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    # here we dont use post_id anymore, to replace it we use
    # args and kwargs to see no error. the reason is our url will send
    # post_id anyway so we need to have it
    def get(self, request, post_id):
        # here we get the related post from our database
        # and send it to the form as instance in order to show
        # the previous text which the body field had.
        post = self.post_isntance
        form = self.form_class(instance=post)
        return render(request, "post/post_update.html", {"form": form})

    def post(self, request, post_id):
        post = self.post_isntance
        # this request.POST
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            # because after updating the slug dont change we need to manage it manually
            # so first we tell save method, dont store and save the new record just keep it
            # because i want to give you new data to store, we do this by commit=False
            new_post = form.save(commit=False)
            # this slugify is for converting our data and body from user to a
            # valid slug with the built-in utils in django
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.save()
            messages.success(request, "you updated this post", "success")
            return redirect("post:post_detail", post.id, post.slug)

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, "post/post_create.html", {"form": form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.slug = slugify(form.cleaned_data["body"][:30])
            new.user = request.user
            new.save()
            messages.success(request, "Post Created Successfully !", "success")
            return redirect("post:post_detail", new.id, new.slug)
        return redirect("home:home")

class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "Reply submitted successfully !", "success")
        return redirect("post:post_detail", post.id, post.slug)