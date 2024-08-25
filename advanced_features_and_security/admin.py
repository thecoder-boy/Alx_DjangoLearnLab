from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User

class CustomUserAdmin(UserAdmin):
  model = User
  fieldsets = UserAdmin.fieldsets + (
    (None, {"fields": ("date_of_birth", "profile_photo")}),
  )


admin.site.register(User, CustomUserAdmin)
