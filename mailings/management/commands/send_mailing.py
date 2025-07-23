import os

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone

from mailings.models import Attempt, Mailing

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


class Command(BaseCommand):
    help = """Команда для отправки рассылки по id. Если рассылка со статусом 'Завершена', то выводится сообщение
    'Данная рассылка завершена'."""

    def add_arguments(self, mailing_id):
        """Функция для получения id рассылки."""
        mailing_id.add_argument("mailing_id", type=int, help="id рассылки")

    def handle(self, *args, **kwargs):
        """Функция для отправки рассылки. Для отправки необходимо указать id рассылки."""
        mailing_id = kwargs["mailing_id"]
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        if mailing.status == "completed":
            print("Данная рассылка завершена")
        else:
            recipients = mailing.recipient.all()
            mailing.created_at = timezone.now()
            mailing.status = "published"
            mailing.save()
            for recipient in recipients:
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient],
                    )
                except Exception as e:
                    Attempt.objects.create(
                        status="unsuccessfully",
                        server_response=f"Ошибка отправки сообщения: {str(e)}",
                        mailing_id=mailing_id,
                        recipient_id=recipient.pk,
                    )
                else:
                    Attempt.objects.create(
                        status="successfully",
                        server_response="Успешно отправлено сообщение",
                        mailing_id=mailing_id,
                        recipient_id=recipient.pk,
                    )
            mailing.finished_at = timezone.now()
            mailing.save()
