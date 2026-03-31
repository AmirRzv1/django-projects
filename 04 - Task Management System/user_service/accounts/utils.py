import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt_token(user):
    """
    Generate a JWT token containing user information.
    This token will be used by other services to identify the user.
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow(),  # Issued at (when token was created)
    }

    # settings.SECRET_KEY is used to sign the token
    # All services must have the SAME secret key to verify this token
    token = jwt.encode(payload,
                       settings.JWT_SECRET_KEY,
                       algorithm=settings.JWT_ALGORITHM)
    return token
