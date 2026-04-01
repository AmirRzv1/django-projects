import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTUser:
    def __init__(self, payload):
        self.id = payload.get('user_id')
        self.username = payload.get('username')
        self.email = payload.get('email')
        self.is_authenticated = True

    def __str__(self):
        return f"JWTUser(id={self.id}, username={self.username})"


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            # Decode and verify the token using shared secret
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            user = JWTUser(payload)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
