from django.db import models


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
        ordering = ["-id"]


class Message(models.Model):
    """Модель сообщение для рассылок. Содержит поля subject(тема письма), body(тело письма), owner."""

    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name="Тема письма")
    body = models.TextField(null=True, blank=True, verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-id"]


class Mailing(models.Model):
    """Модель рассылка. Содержит поля created_at(дата отправки), finished_at(дата окончания отправки), status, message,
    recipient, owner."""

    Created = "created"
    Published = "published"
    Completed = "completed"

    STATUS_CHOICES = [
        (Created, "Создана"),
        (Published, "Запущена"),
        (Completed, "Завершена"),
    ]

    created_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=Created, verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="messages", verbose_name="Сообщение")
    recipient = models.ManyToManyField(Recipient, related_name="recipients", verbose_name="Получатели")

    def __str__(self):
        return f"{self.message}, {self.created_at}, {self.finished_at}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-id"]


class Attempt(models.Model):
    """Модель попытка рассылки. Содержит поля created_at, status, server_response(ответ сервера), recipient."""

    Successfully = "successfully"
    Unsuccessfully = "unsuccessfully"

    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        (Successfully, "Успешно"),
        (Unsuccessfully, "Не успешно"),
    ]
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default=Unsuccessfully)
    server_response = models.TextField(null=True, blank=True)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="attempt_mailings", verbose_name="Рассылка"
    )
    recipient = models.ForeignKey(
        Recipient, on_delete=models.CASCADE, related_name="attempt_recipients", verbose_name="Получатель рассылки"
    )

    def __str__(self):
        return f"{self.mailing}, {self.created_at}, {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["-created_at"]
