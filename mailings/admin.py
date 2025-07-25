from django.contrib import admin

from .models import Attempt, Mailing, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """Админ панель получателей рассылки. Поля для отображения: id, email, full_name. Поле для фильтра: full_name.
    Поле для поиска: email, full_name."""

    list_display = ("id", "email", "full_name")
    list_filter = ("full_name",)
    search_fields = (
        "email",
        "full_name",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админ панель сообщений. Поля для отображения: id, subject, body. Поле для фильтра: subject. Поле для поиска:
    subject."""

    list_display = ("id", "subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Админ панель рассылок. Поля для отображения: id, created_at, status, message. Поле для фильтра: created_at,
    status. Поле для поиска: message."""

    list_display = ("id", "created_at", "status", "message")
    list_filter = ("created_at", "status")
    search_fields = ("message",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """Админ панель попыток рассылок. Поля для отображения: id, created_at, status, server_response. Поле для фильтра:
    created_at, status. Поле для поиска: server_response."""

    list_display = ("id", "created_at", "status", "server_response")
    list_filter = ("created_at", "status")
    search_fields = ("server_response",)
