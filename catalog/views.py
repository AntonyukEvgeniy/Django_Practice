from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    """
    Class-based view for displaying the contacts page
    """

    template_name = "catalog/contacts.html"


class ProductDetailView(TemplateView):
    template_name = "catalog/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = get_object_or_404(Product, pk=kwargs["pk"])
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно создан")
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно обновлен")
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удален")
        return super().delete(request, *args, **kwargs)
