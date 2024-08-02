from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from urlshortener.shortener.models import Shortener
from urlshortener.shortener.services import create_or_get_short_url


@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    list_display = ("snowflake_id", "short_url", "long_url", "created_at", "updated_at")
    search_fields = ("short_url",)
    list_filter = ("short_url", "long_url")

    fieldsets = (
        (None, {"fields": ("snowflake_id", "short_url", "long_url")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            create_or_get_short_url(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
