from django import forms

from .models import Mailing, Message, Recipient


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


class MailingForm(forms.ModelForm):
    """Форма по модели Mailing."""

    class Meta:
        model = Mailing
        exclude = (
            "created_at",
            "finished_at",
            "status",
            "owner",
        )
