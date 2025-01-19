from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


class UserAdmin(UserAdmin):
    pass
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'name', 'mobile', 'user_type',
    #                    'email', 'password1', 'password2',),
    #     }),
    # )
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (('Personal info'),
    #      {'fields': (
    #          'name', 'email', 'mobile', 'profile_photo')}),

    #     (('Permissions'), {
    #      'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type')}),
    #     (('Important dates'), {'fields': ('last_login', 'date_joined')}))

    # list_display = ('id', 'name', 'mobile', 'user_type')


admin.site.register(User, UserAdmin)


