from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from mailings.forms import RecipientForm
from mailings.models import Recipient


# Create your views here.
class MainTemplateView(TemplateView):
    """Контроллер для отображения главной страницы сайта."""

    template_name = "mailings/main.html"


class RecipientCreateView(CreateView):
    """Контроллер для создания получателя рассылок."""

    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientListView(ListView):
    """Контроллер для отображения страницы с получателями."""

    model = Recipient
    template_name = "recipient_list.html"


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
