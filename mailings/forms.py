from django import forms

from .models import Message, Recipient


class RecipientForm(forms.ModelForm):
    """Форма по модели Recipient."""

    class Meta:
        model = Recipient
        exclude = ("owner",)


class MessageForm(forms.ModelForm):
    """Форма по модели Message."""

    class Meta:
        model = Message
        exclude = ("owner",)
