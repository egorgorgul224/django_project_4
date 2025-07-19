from django.urls import path

from mailings.views import MainTemplateView

app_name = "mailings"

urlpatterns = [
    path("main/", MainTemplateView.as_view(), name="main"),
]
