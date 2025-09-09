from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Модель пользователь. Содержит поля email, avatar, phone, country, token."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар", blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name="Страна", blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}, {self.is_active}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["id"]
        permissions = [
            ("can_block_user", "Can block user"),
            ("can_unlock_user", "Can unlock user"),
        ]
