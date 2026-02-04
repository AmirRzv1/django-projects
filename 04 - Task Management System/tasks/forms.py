from django import forms

class TasksCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()

class TaskUpdateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    status = forms.CharField()
