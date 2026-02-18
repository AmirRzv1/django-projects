import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class UserLoginAPIView(View):
    # check that if the user is sending the username or email
    # based on that we return the related information
    def validate_username_or_email(self, data):
        if data and "@" in data:
            return {"email": data.lower()}
        else:
            return {"username": data.lower()}


    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]

        result = self.validate_username_or_email(username)

        if result.get("username", None):
            user = authenticate(username=result["username"], password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True, "user_id": user.id, "username": user.username})


        else:
            user = authenticate(username=result["username"], password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True, "user_id": user.id, "username": user.username})

