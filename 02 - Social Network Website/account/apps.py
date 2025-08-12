from django.apps import AppConfig

# Using this name in setting file for adding this to my project
class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
