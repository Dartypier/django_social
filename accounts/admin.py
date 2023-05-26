from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = (
        "pk",
        "date_joined",
        "last_login",
    )
    list_display = [
        "username",
        "email",
        "is_staff",
        "pk",
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "age",
                    "avatar",
                    "pk",
                    "bio",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "age",
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
