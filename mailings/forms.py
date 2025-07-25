from django import forms

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    """Форма по модели Recipient."""

    class Meta:
        model = Recipient
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите свой email"})

        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ФИО"})

        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})


class MessageForm(forms.ModelForm):
    """Форма по модели Message."""

    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему сообщения"})

        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите сообщение"})


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

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields["message"].widget.attrs.update({"class": "form-select"})

        self.fields["recipient"].widget.attrs.update({"class": "form-select"})
