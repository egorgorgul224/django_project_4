from django.contrib import admin

from .models import Attempt, Mailing, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name")
    list_filter = ("full_name",)
    search_fields = (
        "email",
        "full_name",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status", "message")
    list_filter = ("created_at", "status")
    search_fields = ("message",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status", "server_response")
    list_filter = ("created_at", "status")
    search_fields = ("server_response",)
