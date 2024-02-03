
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from core import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

# Subclassing userAdmin class to customize user model in admin page
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ['email', 'name']
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            }
        ),

        (_("Important dates"), {"fields": ("last_login",)}),
    )

    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("email", "is_staff", "is_superuser")
    ordering = ("id",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)