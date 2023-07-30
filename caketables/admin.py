from django.contrib import admin
from .models import UserTable, Visitor


# 케이크 생성
@admin.register(UserTable)
class UsertableAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Birthday Table",
            {
                "fields": (
                    # "user_pk",
                    # "pk",
                    "owner",
                    "nickname",
                    "tablecolor",
                    # "created_at",
                    # "visitor_name",
                ),
                "classes": ("wide",),
            },
        ),
    )

    list_display = ("pk", "owner", "nickname", "tablecolor", "total_visitor","created_at")
    list_display_links = ("pk", "owner", "nickname", "total_visitor")

    list_filter = ("owner", "nickname")

    search_fields = ("owner", "nickname")


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Decoration",
            {
                "fields": (
                    # "pk",
                    "owner",
                    "pickcake",
                    "letter",
                    "visitor_name",
                    "visitor_password",

                )
            },
        ),
    )
    list_display = ("pk","owner", "visitor_name", "pickcake")
    list_display_links = ("pk","owner", "visitor_name", "pickcake")

    list_filter = ("owner", "pickcake", "visitor_name")

    search_fields = ("owner", "visitor_name")
