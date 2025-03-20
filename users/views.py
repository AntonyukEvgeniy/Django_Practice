from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from environs import env

from .forms import CustomUserCreationForm
from django.contrib.auth import login


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Send welcome email
        subject = "Добро пожаловать на наш сайт. Люблю Машеньку!!!!"
        message = (
            f"Здравствуйте, {user.username}!\n\nСпасибо за регистрацию на нашем сайте."
        )
        from_email = env.str("EMAIL_HOST_USER")  # Замените на ваш email
        recipient_list = [user.email]
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            raise e
        messages.success(self.request, f"Пользователь {user} успешно зарегистрирован!")
        return redirect("catalog:home")


class UserLoginView(LoginView):
    next_page = reverse_lazy("catalog:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy(
        "catalog:home"
    )  # URL для перенаправления после выхода из системы
