from django.shortcuts import render

# Create your views here.
class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/login.html", {"form": form})

    # check that if the user is sending the username or email
    # based on that we return the related information
    def validate_username_or_email(self, data):
        login_info = data.get("username")
        if login_info and "@" in login_info:
            return {"email": login_info.lower()}
        else:
            return {"username": login_info.lower()}


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            result = self.validate_username_or_email(data)

            if result.get("username", None):
                user = authenticate(username=data["username"], password=data["password"])
                if user:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect("home:home")
                else:
                    messages.error(request, "Invalid Credential !!")
                    return redirect("home:home")


            else:
                real_user = User.objects.get(email=data["username"])
                user = authenticate(username=real_user.username, password=data["password"])
                if user:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect("home:home")
                else:
                    messages.error(request, "Invalid Credential !!")
                    return redirect("home:home")
