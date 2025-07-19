from django import forms
from django.core.exceptions import ValidationError

from .models import Recipient


class RecipientForm(forms.ModelForm):
    """Форма по модели Recipient."""

    class Meta:
        model = Recipient
        exclude = ("owner",)
