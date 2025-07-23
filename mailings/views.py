import os
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail

from mailings.forms import MailingForm, MessageForm, RecipientForm
from mailings.models import Mailing, Message, Recipient, Attempt

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


# Create your views here.
class MainTemplateView(TemplateView):
    """Контроллер для отображения главной страницы сайта."""

    template_name = "mailings/main.html"


class RecipientListView(ListView):
    """Контроллер для отображения страницы с получателями."""

    model = Recipient
    template_name = "recipient_list.html"


class RecipientCreateView(CreateView):
    """Контроллер для создания получателя рассылок."""

    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientDetailView(DetailView):
    """Контроллер для просмотра информации о получатели."""

    model = Recipient


class RecipientDeleteView(DeleteView):
    """Контроллер для удаления получателя."""

    model = Recipient
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientUpdateView(UpdateView):
    """Контроллер для обновления информации о получатели."""

    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:recipient_list")

    def get_success_url(self):
        return reverse("mailings:recipient_detail", args=[self.kwargs.get("pk")])


class MessageListView(ListView):
    """Контроллер для отображения страницы с сообщениями."""

    model = Message
    template_name = "message_list.html"


class MessageCreateView(CreateView):
    """Контроллер для создания сообщения."""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageDetailView(DetailView):
    """Контроллер для просмотра информации сообщения."""

    model = Message


class MessageDeleteView(DeleteView):
    """Контроллер для удаления сообщения."""

    model = Message
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(UpdateView):
    """Контроллер для обновления данных сообщения."""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def get_success_url(self):
        return reverse("mailings:message_detail", args=[self.kwargs.get("pk")])


class MailingListView(ListView):
    """Контроллер для отображения страницы с рассылками."""

    model = Mailing
    template_name = "mailing_list.html"


class MailingCreateView(CreateView):
    """Контроллер для создания рассылки."""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDetailView(DetailView):
    """Контроллер для просмотра информации по рассылке."""

    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_emails = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        recipients = mailing_emails.recipient.values_list("email", flat=True)
        context["recipient_email"] = recipients
        return context


class MailingDeleteView(DeleteView):
    """Контроллер для удаления рассылки."""

    model = Mailing
    success_url = reverse_lazy("mailings:mailing_list")


class MailingUpdateView(UpdateView):
    """Контроллер для обновления данных рассылки."""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args=[self.kwargs.get("pk")])


class StartMailingView(View):
    def post(self, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=self.kwargs["pk"])
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
                    mailing_id=self.kwargs["pk"],
                    recipient_id=recipient.pk,
                )
            else:
                Attempt.objects.create(
                    status="successfully",
                    server_response="Успешно отправлено сообщение",
                    mailing_id=self.kwargs["pk"],
                    recipient_id=recipient.pk,
                )
        mailing.finished_at = timezone.now()
        mailing.save()

        return redirect("mailings:mailing_list")
