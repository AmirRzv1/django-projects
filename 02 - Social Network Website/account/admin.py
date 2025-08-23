from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# StackedInline -> is the way about how our model will be attached to the admin panel
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

# Register your models here.
admin.site.register(Relation)