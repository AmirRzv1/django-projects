from django.shortcuts import redirect
from django.contrib import messages

class JWTRequiredMixin:
    """Mixin to ensure JWT token exists in session before accessing view"""

    def dispatch(self, request, *args, **kwargs):
        token = request.session.get("jwt_token")

        if not token:
            messages.error(request, "You must login first.")
            return redirect("core:home")

        return super().dispatch(request, *args, **kwargs)
