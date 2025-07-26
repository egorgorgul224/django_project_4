from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации пользователя. Доступные поля: email, password1, password2."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите свой email"})

        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль еще раз"}
        )


class UserForm(forms.ModelForm):
    """Форма для профиля пользователя. Доступные поля: first_name, last_name, avatar, phone, country."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "phone", "country")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})

        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите фамилию"})

        self.fields["phone"].widget.attrs.update({"class": "form-control", "placeholder": "Введите номер телефона"})

        self.fields["country"].widget.attrs.update({"class": "form-control", "placeholder": "Введите свою страну"})

    def clean_image(self):
        """Функция для проверки корректной загрузки изображения."""

        image = self.cleaned_data.get("image")
        if not image:
            return None
        if not image.name.endswith((".jpg", ".jpeg", ".png")):
            raise ValidationError("Неверный формат файла: используйте JPG или PNG")
        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Файл превышает допустимый размер в 5 МБ")
        return image

    def clean_phone(self):
        """Функция для проверки корректного номера телефона."""

        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять из цифр.")
        return phone
