from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (BlockUserView, RegisterView, UnlockUserView, UserDetailView, UsersListView, UserUpdateView,
                    email_verification)

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailings:main"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("user/<int:pk>/block/", BlockUserView.as_view(), name="user_block"),
    path("user/<int:pk>/unblock/", UnlockUserView.as_view(), name="user_unlock"),
    path("user/<int:pk>/detail/", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
]
