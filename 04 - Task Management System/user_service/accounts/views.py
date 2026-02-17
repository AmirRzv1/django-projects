import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class UserLoginView(View):
    # check that if the user is sending the username or email
    # based on that we return the related information
    def validate_username_or_email(self, data):
        login_info = data.get("username")
        if login_info and "@" in login_info:
            return {"email": login_info.lower()}
        else:
            return {"username": login_info.lower()}


    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        result = self.validate_username_or_email(username)

        if result.get("username", None):
            user = authenticate(username=result.get("username"), password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True, "user_id": user.id, "username": user.username})


        else:
            user = authenticate(username=result.get("username"), password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True, "user_id": user.id, "username": user.username})

