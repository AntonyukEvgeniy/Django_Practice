from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import RegisterView

app_name = "users"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="/", http_method_names=["get", "post"]),
        name="logout",
    ),
]
