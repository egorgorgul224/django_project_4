from django.urls import path

from mailings.views import (MailingCreateView, MailingDeleteView, MailingDetailView, MailingListView,
                            MailingUpdateView, MainTemplateView, MessageCreateView, MessageDeleteView,
                            MessageDetailView, MessageListView, MessageUpdateView, RecipientCreateView,
                            RecipientDeleteView, RecipientDetailView, RecipientListView, RecipientUpdateView)

app_name = "mailings"

urlpatterns = [
    path("main/", MainTemplateView.as_view(), name="main"),
    path("recipient/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/<int:pk>/detail/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/detail/", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/detail/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
]
