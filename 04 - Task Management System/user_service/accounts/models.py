from django.db import models
from django.contrib.auth.models import BaseUserManager

class CostumeUserManager(BaseUserManager):
    def create_user(self, username, password, email=None):
        if not username:
            raise ValueError("Username is required.")
        if not password:
            raise ValueError("Password is required.")

        user = self.model(username=username.lower())
        if email:
            user.email = self.normalize_email()
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password, email=None):
        user = self.create_user(username, password, email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user
