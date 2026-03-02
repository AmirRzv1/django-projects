from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class TasksCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()

class TaskUpdateForm(forms.Form):
    choices = [("ongoing", "OnGoing"),
            ("completed", "Completed")]
    title = forms.CharField()
    description = forms.CharField()
    status = forms.ChoiceField(choices=choices)