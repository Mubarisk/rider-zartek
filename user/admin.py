from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


class _UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("user_type", "lat", "long")}),
    )


admin.site.register(User, _UserAdmin)
# 10.845298123825948, 75.95212104044624