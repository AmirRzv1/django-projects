import requests
import json

from requests.exceptions import RequestException, HTTPError
from .forms import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.http import HttpResponseServerError

class HomeView(View):
    def get(self, request):
        # just show the landing page so simple.
        try:
            return render(request, "landing.html")
        except TemplateSyntaxError:
            return HttpResponseServerError("Landing page template not found.")
        except TemplateDoesNotExist as e:
            return HttpResponseServerError(f"Template syntax error: {str(e)}")
        except Exception as e:
            return HttpResponseServerError(f"Unexpected error: {str(e)}")

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    # because this part repeat a lot i put it here.
    def handle_template_and_error(self, request, message, form):
        messages.error(request, message)
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form_class()
        try:
            return render(request, "accounts/login.html", {"form": form})
        except TemplateSyntaxError:
            return HttpResponseServerError("Landing page template not found.")
        except TemplateDoesNotExist as e:
            return HttpResponseServerError(f"Template syntax error: {str(e)}")
        except Exception as e:
            return HttpResponseServerError(f"Unexpected error: {str(e)}")

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username")
            password = data.get("password")

            try:
                response = requests.post(
                    "http://127.0.0.1:8001/accounts/login/",
                    json={"username": username, "password": password},
                    timeout=5
                )
                response.raise_for_status()  # raise exception for HTTP 4xx/5xx
                response_result = response.json()

            except requests.ConnectionError:
                msg = "Cannot reach authentication server. Try again later."
                return self.handle_template_and_error(request, msg, form)

            except requests.Timeout:
                msg = "Authentication server timed out. Try again later."
                return self.handle_template_and_error(request, msg, form)

            except requests.HTTPError:
                msg = f"Authentication failed: {response.status_code}"
                return self.handle_template_and_error(request, msg, form)

            except json.JSONDecodeError:
                msg = "Invalid response from authentication server."
                return self.handle_template_and_error(request, msg, form)

            except Exception as e:
                msg = f"Unexpected error: {str(e)}"
                return self.handle_template_and_error(request, msg, form)

            if response_result.get("success"):
                request.session["user_id"] = response_result["user_id"]
                request.session["username"] = response_result["username"]
                request.session["user_is_authenticated"] = True
                messages.success(request, "User successfully logged in.")
                return redirect("core:home")

            else:
                msg = response_result.get("error", "Invalid credentials")
                return self.handle_template_and_error(request, msg, form)

class UserLogoutView(View):
    def post(self, request):
        if not request.session.get("user_id"):
            messages.error(request, "You are not logged in.")
            return redirect("core:home")

        request.session.flush()

        messages.success(request, "User successfully logged out.")
        return redirect("core:home")

class UserRegisterView(View):
    form_class = UserRegisterForm

    # validate the output of calling here and then send the final result back
    # to the post method and there i will validate it.
    def register_user(self, data):
        try:
            response = requests.post(
                "http://127.0.0.1:8001/accounts/register/",
                json=data,
                timeout=5
            )

            # Raise for 4xx / 5xx
            response.raise_for_status()

        except HTTPError:
            # Try to extract error message from service
            try:
                error_data = response.json()
                return False, error_data.get("error", "Registration failed.")
            except ValueError:
                return False, f"Service error. Status code: {response.status_code}"

        except requests.Timeout:
            return False, "Service timed out."

        except requests.ConnectionError:
            return False, "Service unavailable."

        except RequestException:
            return False, "Unexpected network error."

        # Validate body existence
        if not response.content:
            return False, "Empty response from service."

        # Validate JSON
        try:
            response_data = response.json()
        except ValueError:
            return False, "Invalid response from service."

        # Logical validation
        if response_data.get("success"):
            return True, "User created successfully."

        return False, response_data.get("error", "Registration failed.")

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            messages.error(request, "Invalid form data.")
            return redirect("core:home")

        success, message = self.register_user(form.cleaned_data)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect("core:home")

class DashboardView(View):

    def get(self, request):
        # user information
        user_id = request.session.get("user_id")

        if not user_id:
            messages.error(request, "You need to login first!")
            return redirect("core:home")
        try:
            user_response = requests.get("http://127.0.0.1:8001/accounts/information/",
                                    json={ "user_id": user_id },
                                    timeout=5)
            if not user_response.content:
                raise ValueError("Empty Response.")

            user_response_result = user_response.json()

        except(RequestException, HTTPError):
                messages.error(request, "Unable to load user information.")
                return redirect("core:home")

        except ValueError:
            messages.error(request, "Invalid user information response.")
            return redirect("core:home")

        request.session["username"] = user_response_result.get("username")
        request.session["email"] = user_response_result.get("email", "No email.")

        # user tasks
        try:
            user_task_response = requests.get("http://127.0.0.1:8000/tasks/tasks/",
                                              json={"user_id": user_id},
                                              timeout=5)

            user_task_response.raise_for_status()

            if user_task_response.content:
                user_task_response_result = user_task_response.json()

        except (RequestException, HTTPError):
            messages.warning(request, "Tasks service unavailable. Showing empty task list.")

        except ValueError:
            messages.warning(request, "Invalid tasks response. Showing empty task list.")

        request.session["tasks"] = user_task_response_result
        request.session["tasks_count"] = len(user_task_response_result)

        return render(request, "tasks/dashboard.html", {"tasks": user_task_response_result})

class UserTaskCreateView(View):
    form_class = TasksCreateForm
    template_class = "tasks/task_create.html"

    # because this part repeat a lot i put it here.
    def handle_template_and_error(self, request, message, form):
        messages.error(request, message)
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        user_id = request.session.get("user_id")

        # Must be logged in
        if not user_id:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_class, {"form": form})

        data = form.cleaned_data

        try:
            response = requests.post("http://127.0.0.1:8000/tasks/tasks/",
                                     json={
                                         "user_id": user_id,
                                         "title": data["title"],
                                         "description": data["description"]
                                     })
            response.raise_for_status()

        except (RequestException, HTTPError):
            msg = "Task service unavailable. Please try again."
            return self.handle_template_and_error(request, msg, form)

        # Validate response body
        if not response.content:
            msg = "Empty response from task service."
            return self.handle_template_and_error(request, msg, form)

        try:
            response_result = response.json()
        except ValueError:
            msg = "Invalid response from task service."
            return self.handle_template_and_error(request, msg, form)


        # Logical validation
        if response_result.get("success"):
            messages.success(request, "Task created successfully.")
            return redirect("core:dashboard")

        msg = response_result.get("error", "Task creation failed.")
        return self.handle_template_and_error(request, msg, form)







