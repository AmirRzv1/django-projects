from django  import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.Form):
    # class if for defining a bootsrap class for example for better ui
    # placeholder -> to put a phantom text in the field to user
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","placeholder": "SidAmir"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "s.amirhosein.rzv@gmail.com"}))
    # help_text --> this will be shown near the input when its being rendered
    # widget --> PasswordInput -> this is an extra feature for our form that hide
    # the password we are entering in the form that being shown to us
    password1 = forms.CharField(label="Password" , widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", help_text="Dont Use : #$%^&*",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    # we use this to validate 2 fields which is connected to each other
    def clean(self):
        # this gives us the cleaned_data
        cd = super().clean()

        # using get so if the user dont enter one of these
        # we see no error and have None instead
        p1 = cd.get("password1")
        p2 = cd.get("password2")

        # check if they are present and they are not the same
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords must match !")


    # use this type of naming for creating our costume validation
    # clean_ + field name
    def clean_email(self):
        # with self we have access to cleaned_data
        email = self.cleaned_data["email"]
        user_email_exist = User.objects.filter(email=email)
        if user_email_exist:
            # we show the user related validation error
            raise ValidationError("This Email already exists")
        # after all of this we return the data we were working on
        return email

    # This one checks that we dont have the same username and show good error message
    def clean_username(self):
        username = self.cleaned_data["username"]
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise ValidationError("This Username already exists try new one !")
        return username

