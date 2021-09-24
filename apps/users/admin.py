from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["first_name", "last_name", "email"]
    model = User
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "last_login",
        "created_at",
    ]
    list_filter = ["first_name", "last_name", "email", "is_staff", "is_active"]
    fieldsets = (
        ("Login Credentials", {"fields": ("email", "password")}),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "id_number",
                )
            },
        ),
        (
            "Permissions and Groups",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("created_at", "updated_at", "last_login")}),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        },
    )
    search_fields = ["first_name", "last_name", "email"]
    readonly_fields = ["created_at", "updated_at", "last_login"]


admin.site.register(User, UserAdmin)
