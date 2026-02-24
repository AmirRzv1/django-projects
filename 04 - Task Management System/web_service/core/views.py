import requests
import json

from requests.exceptions import RequestException
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
    # because this part repeat a lot i put it here.
    def handle_template_and_error(self, request, message):
        messages.error(request, message)
        return redirect("core:home")

    def post(self, request):
        user_id = request.session.get("user_id")

        if not user_id:
            msg = "You are not logged in."
            return self.handle_template_and_error(request, msg)

        try:
            response = requests.post("http://127.0.0.1:8001/accounts/logout/",
                                     json={"user_id": user_id},
                                     timeout=5
                                     )
            # Raise exception for 4xx / 5xx
            response.raise_for_status()

            # Check empty body
            if not response.content:
                raise ValueError("Empty response from authentication server.")

            final_response = response.json()

        except requests.ConnectionError:
            msg = "Cannot reach authentication server."
            return self.handle_template_and_error(request, msg)

        except requests.Timeout:
            msg = "Authentication server timed out."
            return self.handle_template_and_error(request, msg)

        except requests.HTTPError:
            msg = f"Logout failed. Status code: {response.status_code}"
            return self.handle_template_and_error(request, msg)

        except ValueError:
            msg = "Invalid response from authentication server."
            return self.handle_template_and_error(request, msg)

        except RequestException:
            msg = "Unexpected error while contacting authentication server."
            return self.handle_template_and_error(request, msg)

        # Logical response validation
        if not final_response.get("success"):
            messages.error(request, final_response.get("error", "Logout failed."))
            return redirect("core:home")

        # ✅ Logout success → destroy entire session
        # using flush to clear the whole session and delete what is left
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

            if response.status_code != 200:
                return False, "Service error."

            try:
                response_data = response.json()
            except ValueError:
                return False, "Invalid response from service."

            if response_data.get("success"):
                return True, "User created successfully."

            return False, response_data.get("error", "Registration failed.")

        except requests.exceptions.Timeout:
            return False, "Service timed out."
        except requests.exceptions.ConnectionError:
            return False, "Service unavailable."
        except requests.exceptions.RequestException:
            return False, "Unexpected network error."

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

        user_response = requests.get("http://127.0.0.1:8001/accounts/information/",
                                json={ "user_id": user_id },
                                timeout=5)

        user_response_result = user_response.json()
        request.session["username"] = user_response_result.get("username")
        request.session["email"] = user_response_result.get("email", "No email.")
        print(user_response_result)

        # user tasks
        user_task_response = requests.get("http://127.0.0.1:8000/tasks/tasks/",
                                          json={"user_id": user_id},
                                          timeout=5)
        if not user_task_response:
            user_task_response_result = []
        else:
            user_task_response_result = user_task_response.json()
            request.session["tasks"] = user_task_response_result
            request.session["tasks_count"] = len(user_task_response_result)

        return render(request, "tasks/dashboard.html", {"tasks": user_task_response_result})

class UserTaskCreateView(View):
    form_class = TasksCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, "tasks/task_create.html", {"form": form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data["title"]
            description = data["description"]
            user_id = request.session.get("user_id")

            response = requests.post("http://127.0.0.1:8000/tasks/tasks/",
                                     json={
                                         "user_id": user_id,
                                         "title": title,
                                         "description": description
                                     })
            response_result = response.json()
            if response_result.get("success"):
                messages.success(request, "Task created.")
                return redirect("core:dashboard")
            else:
                messages.error(request, "Task creation Error !!!")
                return redirect("core:task_create")






