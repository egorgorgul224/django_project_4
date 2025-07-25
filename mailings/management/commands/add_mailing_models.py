from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand

from mailings.models import Attempt, Mailing, Message, Recipient


class Command(BaseCommand):
    help = "Add test recipients, messages, mailings and attempts to the database"

    def handle(self, *args, **kwargs):
        Recipient.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()
        Attempt.objects.all().delete()

        try:
            call_command(
                "loaddata",
                (
                    "attempts_fixture.json",
                    "mailings_fixture.json",
                    "messages_fixture.json",
                    "recipients_fixture.json",
                ),
            )
            self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстур."))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка загрузки фикстур: {e}."))
