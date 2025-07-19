from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from mailings.forms import MailingForm, MessageForm, RecipientForm
from mailings.models import Mailing, Message, Recipient


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
