import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from mailings.forms import MailingForm, MessageForm, RecipientForm
from mailings.models import Attempt, Mailing, Message, Recipient

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


# Create your views here.
class MainTemplateView(TemplateView):
    """Контроллер для отображения главной страницы сайта."""

    template_name = "mailings/main.html"

    def get_context_data(self, **kwargs):
        """Функция для получения данных по рассылкам, получателям и сообщениям. Используются для отображения
        статистики на главной странице."""

        context = super().get_context_data(**kwargs)
        user_email = self.request.user
        mailing_info = len(Mailing.objects.filter(owner=self.request.user.id))
        recipient_unique = len(Recipient.objects.filter(owner=self.request.user.id))
        message_info = len(Message.objects.filter(owner=self.request.user.id))
        mailing_active = len(Mailing.objects.filter(status=Mailing.Published).filter(owner=self.request.user.id))
        recipient_in_mailing = len(
            set(Attempt.objects.filter(owner=self.request.user.id).values_list("recipient", flat=True))
        )
        message_success = len(
            Attempt.objects.filter(status=Attempt.Successfully)
            .filter(owner=self.request.user.id)
            .values_list("mailing", flat=True)
        )
        attempt_sent = len(Attempt.objects.filter(owner=self.request.user.id))
        attempt_success = len(Attempt.objects.filter(status=Attempt.Successfully).filter(owner=self.request.user.id))
        attempt_unsuccess = len(
            Attempt.objects.filter(status=Attempt.Unsuccessfully).filter(owner=self.request.user.id)
        )
        context = {
            "mailing_info": mailing_info,
            "recipient_unique": recipient_unique,
            "message_info": message_info,
            "mailing_active": mailing_active,
            "recipient_in_mailing": recipient_in_mailing,
            "attempt_sent": attempt_sent,
            "attempt_success": attempt_success,
            "attempt_unsuccess": attempt_unsuccess,
            "message_success": message_success,
            "user_email": user_email,
        }

        return context


class RecipientListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения страницы с получателями."""

    paginate_by = 15
    model = Recipient
    template_name = "recipient_list.html"

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user.id)


class RecipientCreateView(CreateView):
    """Контроллер для создания получателя рассылок."""

    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        recipient = form.save(commit=False)
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


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


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения страницы с сообщениями."""

    paginate_by = 15
    model = Message
    template_name = "message_list.html"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user.id)


class MessageCreateView(CreateView):
    """Контроллер для создания сообщения."""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        message = form.save(commit=False)
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


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


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения страницы с рассылками."""

    paginate_by = 15
    model = Mailing
    template_name = "mailing_list.html"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user.id)


class MailingCreateView(CreateView):
    """Контроллер для создания рассылки."""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    """Контроллер для просмотра информации по рассылке."""

    model = Mailing

    def get_context_data(self, **kwargs):
        """Функция для получения всех получателей рассылки."""
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


class AttemptListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения страницы с попытками рассылки."""

    paginate_by = 15
    model = Attempt
    template_name = "attempt_list.html"

    def get_queryset(self):
        return Attempt.objects.filter(owner=self.request.user.id)


class StartMailingView(View):
    """Функция для рассылки сообщений всем получателям данной рассылки. После отправки сообщения создается объект
    модели Attempt с результатами рассылки."""

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
                    owner=self.request.user,
                )
            else:
                Attempt.objects.create(
                    status="successfully",
                    server_response="Успешно отправлено сообщение",
                    mailing_id=self.kwargs["pk"],
                    recipient_id=recipient.pk,
                    owner=self.request.user,
                )
        mailing.finished_at = timezone.now()
        mailing.save()

        return redirect("mailings:mailing_list")


class AddArchiveView(View):
    """Функция для добавления рассылки в архив. Статус меняется на 'Завершено'."""

    def post(self, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        mailing.status = "completed"
        mailing.save()

        return redirect("mailings:mailing_list")
