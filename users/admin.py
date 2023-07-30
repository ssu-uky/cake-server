from django.contrib import admin
from .models import User, FeedbackUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "name",
                    "email",
                    "password",
                    # "birthday",
                    "is_admin",
                    "social_type",
                    "is_active",
                    # "cake",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_superuser", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("pk", "name", "email", "social_type", "is_active", "is_admin")
    list_display_links = ("pk", "social_type", "name", "email")
    list_filter = ("social_type",)


@admin.register(FeedbackUser)
class FeedbackUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Feedback",
            {
                "fields": (
                    "feedback_name",
                    "feedback_email",
                    "feedback_content",
                    "created_at",
                ),
                "classes": ("wide",),
            },
        ),
    )
    readonly_fields = ("created_at",)
    list_display = (
        "pk",
        "feedback_name",
        "feedback_content",
        "feedback_email",
        "created_at",
    )
    list_display_links = ("pk", "created_at", "feedback_name", "feedback_content")
    list_filter = ("created_at",)
