from django import forms

class TasksCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
