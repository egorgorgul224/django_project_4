from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View


# Create your views here.
class MainTemplateView(TemplateView):
    template_name = "mailings/main.html"
