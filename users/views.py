from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Send welcome email
        subject = "Люблю Python!!!!"
        message = (
            f"Здравствуйте, {user.username}!\n\nСпасибо за регистрацию на нашем сайте."
        )
        try:
            user.email_user(subject, message)
        except SMTPException as e:
            messages.error(self.request, f"Ошибка отправки email: {str(e)}")
        messages.success(self.request, f"Пользователь {user} успешно зарегистрирован!")
        return redirect("catalog:home")


class UserLoginView(LoginView):
    next_page = reverse_lazy("catalog:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy(
        "catalog:home"
    )  # URL для перенаправления после выхода из системы
