from django import forms
from .models import *

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body"]

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body"]

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        # after defining our fields and model we use this for
        # using widgets  in our model form
        # syntax -> model: widgets
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control"})
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]