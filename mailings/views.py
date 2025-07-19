from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from mailings.forms import MessageForm, RecipientForm
from mailings.models import Message, Recipient


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
    """Контроллер для обновления информации сообщения."""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def get_success_url(self):
        return reverse("mailings:message_detail", args=[self.kwargs.get("pk")])
