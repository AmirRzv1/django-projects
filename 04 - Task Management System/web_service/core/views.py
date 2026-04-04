import requests
import json
import jwt
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from requests.exceptions import RequestException, HTTPError
from .forms import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.http import HttpResponseServerError

# ✓ Fixed | No changes for DRF
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

# ✓ DRF Applied
class UserRegisterView(View):
    """
    take the username, password and email(optional) from user and use this
    to create a user with user_service and show the response.
    """
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

                if "error" in error_data:  # Changed from "errors"
                    errors = error_data["error"]
                else:
                    errors = error_data

                error_messages = []
                for field, messages_list in errors.items():
                    # Handle both string and list
                    if isinstance(messages_list, str):
                        messages_list = [messages_list]

                    if field == "non_field_errors":
                        error_messages.extend(messages_list)
                    else:
                        error_messages.append(f"{field}: {', '.join(messages_list)}")

                return False, " | ".join(error_messages)

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

# ✓ DRF Applied
class UserLoginView(View):
    """
    Take the essential information from the user and send them to the
    user_service to be authenticated and save the information in the session.
    """
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def handle_template_and_error(self, request, message, form):
        messages.error(request, message)
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form_class()
        try:
            return render(request, self.template_name, {"form": form})
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
                    json={
                        "username_or_email": username,
                        "password": password
                    },
                    timeout=5,
                )

            except requests.ConnectionError:
                msg = "Cannot reach authentication server. Try again later."
                return self.handle_template_and_error(request, msg, form)

            except requests.Timeout:
                msg = "Authentication server timed out. Try again later."
                return self.handle_template_and_error(request, msg, form)

            except Exception as e:
                msg = f"Unexpected error: {str(e)}"
                return self.handle_template_and_error(request, msg, form)

            # Handle failed response (4xx, 5xx)
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    msg = error_data.get("errors", "Invalid credentials.")
                except (ValueError, KeyError):
                    msg = f"Authentication failed (status {response.status_code})"
                return self.handle_template_and_error(request, msg, form)

            # Handle successful response
            try:
                response_data = response.json()
            except ValueError:
                msg = "Invalid response from authentication server."
                return self.handle_template_and_error(request, msg, form)

            # Check if token exists in response
            token = response_data.get("token")
            user_info = response_data.get("user")
            print(f"user = {user_info.get('username')} | token = {token}")

            if token and user_info:
                # Save to session
                request.session["jwt_token"] = token
                request.session["user_id"] = user_info.get("id")
                request.session["username"] = user_info.get("username")
                request.session["email"] = user_info.get("email")
                request.session["user_is_authenticated"] = True

                messages.success(request, "User successfully logged in.")
                return redirect("core:home")
            else:
                msg = "Invalid response structure from server."
                return self.handle_template_and_error(request, msg, form)

        # Form is not valid
        return render(request, self.template_name, {"form": form})

# ✓ DRF Applied
class UserLogoutView(View):
    def post(self, request):
        if not request.session.get("user_id"):
            messages.error(request, "You are not logged in.")
            return redirect("core:home")

        request.session.flush()

        messages.success(request, "User successfully logged out.")
        return redirect("core:home")

# ✓ DRF Applied
class DashboardView(View):
    """
    showing the dashboard for user with the information the user provide by
    the token it has and we extract it and put data in the places and
    show it in final template and also extract the data we needed from task_service.
    """


    def get(self, request):
        user_id = request.session.get("user_id")
        token = request.session.get("jwt_token")

        if not user_id or not token:
            messages.error(request, "You need to login first!")
            return redirect("core:home")

        # ---- Extract user info from token ----
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            messages.error(request, "Session expired. Please login again.")
            request.session.flush()
            return redirect("core:home")
        except jwt.InvalidTokenError:
            messages.error(request, "Invalid session. Please login again.")
            request.session.flush()
            return redirect("core:home")

        username = payload.get("username")
        email = payload.get("email")

        headers = {"Authorization": f"Bearer {token}"}

        # Update session with fresh data
        request.session["username"] = username
        request.session["email"] = email

        # ---- Fetch Tasks ----
        active_tasks = []
        active_count = 0
        deleted_tasks = []
        deleted_count = 0

        try:
            task_response = requests.get(
                "http://127.0.0.1:8000/tasks/tasks/",
                headers=headers,
                timeout=5
            )

            if task_response.status_code == 200:
                task_data = task_response.json()
                active_tasks = task_data.get("active_tasks", [])
                active_count = task_data.get("active_count", 0)
                deleted_tasks = task_data.get("deleted_tasks", [])
                deleted_count = task_data.get("deleted_count", 0)

        except requests.exceptions.RequestException:
            messages.warning(request, "Tasks service unavailable.")

        return render(request, "tasks/dashboard.html", {
            "active_tasks": active_tasks,
            "active_count": active_count,
            "deleted_tasks": deleted_tasks,
            "deleted_count": deleted_count,
        })

# ✓ DRF Applied
class UserTaskCreateView(View):
    form_class = TasksCreateForm
    template_class = "tasks/task_create.html"

    # because this part repeat a lot i put it here.
    def handle_template_and_error(self, request, message, form):
        messages.error(request, message)
        return render(request, self.template_class, {"form": form})

    def get(self, request):
        token = request.session.get("jwt_token")
        if not token:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        form = self.form_class()
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        token = request.session.get("jwt_token")
        if not token:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_class, {"form": form})

        data = form.cleaned_data
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.post("http://127.0.0.1:8000/tasks/task_create/",
                                     headers=headers,
                                     json={
                                         "title": data["title"],
                                         "description": data["description"]
                                     },
                                     timeout=5)
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

# ✓ DRF Applied
class TaskSoftDelete(View):

    def post(self, request, task_id):
        token = request.session.get("jwt_token")
        if not token:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        try:
            response = requests.post(f"http://127.0.0.1:8000/tasks/task-soft-delete/{task_id}/",
                                     headers={"Authorization": f"Bearer {token}"},
                                     timeout=5)
            response.raise_for_status()
            try:
                result = response.json()
            except ValueError:
                messages.error(request, "Invalid response from server")
                return redirect("core:dashboard")

            if result.get("success"):
                messages.success(request, "Task soft deleted")
                return redirect("core:dashboard")

            # Show specific error from backend
            error_msg = result.get("error", "Failed to soft delete task")
            messages.error(request, error_msg)
            return redirect("core:dashboard")

        # Handle network/timeout errors
        except requests.exceptions.Timeout:
            messages.error(request, "Request timeout. Please try again")
            return redirect("core:dashboard")

        except requests.exceptions.ConnectionError:
            messages.error(request, "Cannot connect to task service")
            return redirect("core:dashboard")

        # Handle HTTP errors (400, 404, 500)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                messages.error(request, "Task not found")
            elif e.response.status_code == 400:
                messages.error(request, "Invalid request")
            else:
                messages.error(request, "Server error. Please try again")
            return redirect("core:dashboard")

        except Exception:
            messages.error(request, "An unexpected error occurred")
            return redirect("core:dashboard")

# ✓ DRF Applied
class TaskUpdateView(View):
    class_template = "tasks/task_update.html"
    class_form = TaskUpdateForm

    def get(self, request, task_id):
        # getting real_task to prefill the entries
        token = request.session.get("jwt_token")
        if not token:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        try:
            # Use query parameters for GET (REST standard)
            response = requests.get(
                f"http://127.0.0.1:8000/tasks/task-detail/{task_id}/",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            response.raise_for_status()

            # Handle JSON parsing
            try:
                result = response.json()
            except ValueError:
                messages.error(request, "Invalid response from server")
                return redirect("core:dashboard")

            form = self.class_form(initial={
                "title": result["title"],
                "description": result["description"],
                "status": result["status"]
            })
            return render(request, self.class_template, {"form": form})

        except requests.exceptions.Timeout:
            messages.error(request, "Request timeout. Please try again")
            return redirect("core:dashboard")

        except requests.exceptions.ConnectionError:
            messages.error(request, "Cannot connect to task service")
            return redirect("core:dashboard")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                messages.error(request, "Task not found")
            else:
                messages.error(request, "Server error. Please try again")
            return redirect("core:dashboard")

        except Exception:
            messages.error(request, "An unexpected error occurred")
            return redirect("core:dashboard")

    def post(self, request, task_id):
        form = self.class_form(request.POST)
        token = request.session.get("jwt_token")
        if not token:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.post(
                    f"http://127.0.0.1:8000/tasks/task-update/{task_id}/",
                    json={
                        "title": data["title"],
                        "description": data["description"],
                        "status": data["status"]
                    },
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5
                )
                response.raise_for_status()

                # Handle JSON parsing
                try:
                    result = response.json()
                except ValueError:
                    messages.error(request, "Invalid response from server")
                    return render(request, self.class_template, {"form": form})

                if result.get("success"):
                    messages.success(request, "Task updated successfully")
                    return redirect("core:dashboard")

                # Show specific error from backend
                error_msg = result.get("error", "Failed to update task")
                messages.error(request, error_msg)
                return render(request, self.class_template, {"form": form})

            except requests.exceptions.Timeout:
                messages.error(request, "Request timeout. Please try again")
                return render(request, self.class_template, {"form": form})

            except requests.exceptions.ConnectionError:
                messages.error(request, "Cannot connect to task service")
                return render(request, self.class_template, {"form": form})

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    messages.error(request, "Task not found")
                elif e.response.status_code == 400:
                    messages.error(request, "Invalid request")
                else:
                    messages.error(request, "Server error. Please try again")
                return render(request, self.class_template, {"form": form})

            except Exception:
                messages.error(request, "An unexpected error occurred")
                return render(request, self.class_template, {"form": form})

        # ✓ Handle invalid form
        messages.error(request, "Please correct the errors below")
        return render(request, self.class_template, {"form": form})

# need improvements, we don't need to take the whole tasks and then
# filter them.
class RecycleBinView(View):
    class_template = "tasks/recycle_bin.html"

    def get(self, request):
        # user tasks
        user_id = request.session.get("user_id")

        tasks = []
        task_soft_delete_count = 0

        try:
            user_task_response = requests.get("http://127.0.0.1:8000/tasks/tasks/",
                                              json={"user_id": user_id},
                                              timeout=5)

            user_task_response.raise_for_status()

            if user_task_response.content:
                user_task_response_result = user_task_response.json()
                tasks = user_task_response_result.get("tasks")

            for task in tasks:
                if task["status"] == "soft_delete":
                    task_soft_delete_count += 1

        except (RequestException, HTTPError):
            messages.warning(request, "Tasks service unavailable.")

        except ValueError:
            messages.warning(request, "Invalid tasks response.")

        return render(request, self.class_template, {"tasks": tasks, "task_soft_delete_count": task_soft_delete_count})

# ✓ Fixed
class TaskRestoreView(View):
    def post(self, request, task_id):
        try:
            response = requests.post("http://127.0.0.1:8000/tasks/task-restore/",
                                     json={"task_id": task_id, "user_id": request.session["user_id"]},
                                     timeout=5)
            response.raise_for_status()
            # Handle JSON parsing
            try:
                result = response.json()
            except ValueError:
                messages.error(request, "Invalid response from server")
                return redirect("core:recycle_bin")

            if result.get("success"):
                messages.success(request, "Task restored successfully")
                return redirect("core:recycle_bin")

            # Show specific error from backend
            error_msg = result.get("error", "Failed to restore task")
            messages.error(request, error_msg)
            return redirect("core:recycle_bin")

        except requests.exceptions.Timeout:
            messages.error(request, "Request timeout. Please try again")
            return redirect("core:recycle_bin")

        except requests.exceptions.ConnectionError:
            messages.error(request, "Cannot connect to task service")
            return redirect("core:recycle_bin")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                messages.error(request, "Task not found")
            elif e.response.status_code == 400:
                messages.error(request, "Invalid request")
            else:
                messages.error(request, "Server error. Please try again")
            return redirect("core:recycle_bin")

        except Exception:
            messages.error(request, "An unexpected error occurred")
            return redirect("core:recycle_bin")

# ✓ Fixed
class TaskHardDeleteView(View):
    def post(self, request, task_id):
        user_id = request.session.get("user_id")
        try:
            response = requests.post("http://127.0.0.1:8000/tasks/task-hard-delete/",
                                     json={"user_id": user_id, "task_id": task_id},
                                     timeout=5)
            response.raise_for_status()
            # Handle JSON parsing
            try:
                result = response.json()
            except ValueError:
                messages.error(request, "Invalid response from server")
                return redirect("core:recycle_bin")

            if result.get("success"):
                messages.success(request, "Task deleted permanently")
                return redirect("core:recycle_bin")

            # Show specific error from backend
            error_msg = result.get("error", "Failed to delete task")
            messages.error(request, error_msg)
            return redirect("core:recycle_bin")

        except requests.exceptions.Timeout:
            messages.error(request, "Request timeout. Please try again")
            return redirect("core:recycle_bin")

        except requests.exceptions.ConnectionError:
            messages.error(request, "Cannot connect to task service")
            return redirect("core:recycle_bin")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                messages.error(request, "Task not found")
            elif e.response.status_code == 400:
                messages.error(request, "Invalid request")
            else:
                messages.error(request, "Server error. Please try again")
            return redirect("core:recycle_bin")

        except Exception:
            messages.error(request, "An unexpected error occurred")
            return redirect("core:recycle_bin")


