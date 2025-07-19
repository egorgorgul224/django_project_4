from django.db import models

from users.models import User


# Create your models here.
class Recipient(models.Model):
    """Модель получателя рассылок. Содержит поля email, full_name, comment, owner."""

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["email"]


class Message(models.Model):
    """Модель сообщение для рассылок. Содержит поля subject(тема письма), body(тело письма), owner."""

    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name="Тема письма")
    body = models.TextField(null=True, blank=True, verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    """Модель рассылка. Содержит поля created_at(дата отправки), finished_at(дата окончания отправки), status, message,
    recipient, owner."""

    created_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    STATUS_CHOICES = [
        ("created", "Created"),
        ("published", "Published"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="messages", verbose_name="Сообщение")
    recipient = models.ManyToManyField(Recipient, related_name="recipients", verbose_name="Получатели")

    def __str__(self):
        return f"{self.message}, {self.created_at}, {self.finished_at}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["finished_at"]


class Attempt(models.Model):
    """Модель попытка рассылки. Содержит поля created_at, status, server_response(ответ сервера), recipient."""

    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("successfully", "Successfully"),
        ("unsuccessfully", "Unsuccessfully"),
    ]
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default="unsuccessfully")
    server_response = models.TextField()
    recipient = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="mailings", verbose_name="Рассылка")

    def __str__(self):
        return f"{self.recipient}, {self.created_at}, {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["created_at"]
