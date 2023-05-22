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

    list_display = ("pk", "name", "email","social_type", "is_admin")
    list_display_links = ("pk","social_type", "name", "email")
    list_filter = ("social_type",)


@admin.register(FeedbackUser)
class FeedbackUserAdmin(admin.ModelAdmin):
    class Meta:
        model = FeedbackUser
        fieldsets = (
            (
                "Feedback",
                {
                    "fields": (
                        "feedback_name",
                        "feedback_email",
                        "feedback_content",
                        "feedback_password",
                    ),
                    "classes": ("wide",),
                },
            ),
        )

        list_display = ("pk", "created_at", "feedback_name", "feedback_content")
        list_display_links = ("pk", "created_at", "feedback_name", "feedback_content")
        list_filter = ("created_at",)
