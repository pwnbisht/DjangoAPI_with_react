from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from api.models import User


class UserAdminModel(BaseAdmin):

    list_display = ["email", "name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "name"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdminModel)
