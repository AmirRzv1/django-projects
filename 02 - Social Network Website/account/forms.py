from django  import forms

class UserRegisterForm(forms.Form):
    # class if for defining a bootsrap class for example for better ui
    # placeholder -> to put a phantom text in the field to user
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","placeholder": "SidAmir"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "s.amirhosein.rzv@gmail.com"}))
    # help_text --> this will be shown near the input when its being rendered
    # widget --> PasswordInput -> this is an extra feature for our form that hide
    # the password we are entering in the form that being shown to us
    password = forms.CharField(help_text="Dont Use : #$%^&*", widget=forms.PasswordInput(attrs={"class": "form-control"}))