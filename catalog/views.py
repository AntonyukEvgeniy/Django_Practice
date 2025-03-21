from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
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
    """
    Главная страница
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Возвращает только опубликованные продукты"""
        if self.request.user.groups.filter(name="Product Moderator").exists():
            return Product.objects.all()
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_moderator"] = self.request.user.groups.filter(
            name="Product Moderator"
        ).exists()
        return context


class ContactsView(TemplateView):
    """
    CBV, отображаем страницу контактов
    """

    template_name = "catalog/contacts.html"


class ProductDetailView(LoginRequiredMixin, TemplateView):
    template_name = "catalog/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = get_object_or_404(Product, pk=kwargs["pk"])
        context["is_moderator"] = self.request.user.groups.filter(
            name="Product Moderator"
        ).exists()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно создан")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.groups.filter(name="Product Moderator").exists():
            return base_qs
        return base_qs.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        if "is_published" in self.request.POST:
            form.instance.is_published = self.request.POST.get("is_published") == "on"
            if form.instance.is_published != self.get_object().is_published:
                if not self.request.user.has_perm("catalog.can_unpublish_product"):
                    messages.error(
                        self.request,
                        "У вас нет прав на публикацию/снятие с публикации продукта",
                    )
                    return self.form_invalid(form)
        messages.success(self.request, "Продукт успешно обновлен")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.groups.filter(name="Product Moderator").exists():
            return base_qs
        return base_qs.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        if (
            not request.user.has_perm("catalog.delete_product")
            and not self.get_queryset().exists()
        ):
            messages.error(request, "У вас нет прав на удаление продукта")
            return redirect("catalog:product_detail", pk=kwargs["pk"])
        messages.success(request, "Продукт успешно удален")
        return super().delete(request, *args, **kwargs)
