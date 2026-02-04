from django import forms
from .models import Task

class TasksCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status"]
