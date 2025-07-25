from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Add test users to the database"

    def handle(self, *args, **kwargs):
        User.objects.all().delete()

        try:
            call_command(
                "loaddata",
                ("users_fixture.json",),
            )
            self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры."))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка загрузки фикстур: {e}."))
