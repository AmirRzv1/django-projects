from django import forms

class PostUpdateForm(forms.Form):
    body = forms.CharField()