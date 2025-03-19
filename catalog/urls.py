from django.urls import path
from . import views
from .views import ContactsView

app_name = 'catalog'
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]