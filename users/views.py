import os
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import CustomUserCreationForm, UserForm
from .models import User

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


class RegisterView(CreateView):
    """Класс для регистрации пользователя."""

    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mailings:main")

    def form_valid(self, form):
        """Функция валидации пользователя и отправки сообщения для подтверждения почты."""

        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Функция верификации пользователя после подтверждения почты. После подтверждения почты поле is.active становится
    True и присваивается группа прав 'Пользователь'."""

    user = get_object_or_404(User, token=token)
    user.is_active = True
    group = Group.objects.get(name="User")
    user.groups.add(group)
    user.save()
    return redirect(reverse("users:login"))


class UserDetailView(DetailView):
    """Контроллер для просмотра информации пользователя."""

    model = User


class UserUpdateView(UpdateView):
    """Контроллер для обновления информации о пользователи."""

    model = User
    form_class = UserForm
    success_url = reverse_lazy("mailings:main")

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.kwargs.get("pk")])


class UsersListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения страницы со всеми пользователями сервиса."""

    paginate_by = 15
    model = User
    template_name = "user_list.html"

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.groups.filter(name="Manager").exists() or user.is_superuser):
            return HttpResponseForbidden("У вас нет прав для посещения данной страницы")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser:
            user_group = User.objects.filter(groups__name="User")
            return user_group
        else:
            return User.objects.filter(Q(groups__name="User") | Q(groups__name="Manager"))


class BlockUserView(LoginRequiredMixin, View):
    """Контроллер для блокировки пользователя на сервере. Доступно для пользователей с правами доступа 'Менеджер' и
    'Админ'."""

    def post(self, request, pk: int, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)

        if not (user.groups.filter(name="Manager").exists() or user.is_superuser):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователей")

        user.is_active = False
        user.save()

        return redirect("users:user_list")


class UnlockUserView(LoginRequiredMixin, View):
    """Контроллер для разблокировки пользователя на сервере. Доступно для пользователей с правами доступа 'Менеджер' и
    'Админ'."""

    def post(self, request, pk: int, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)

        if not (user.groups.filter(name="Manager").exists() or user.is_superuser):
            return HttpResponseForbidden("У вас нет прав для разблокировки пользователей")

        user.is_active = True
        user.save()

        return redirect("users:user_list")
