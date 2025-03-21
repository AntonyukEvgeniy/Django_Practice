from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import Product


class HomeView(TemplateView):
    template_name = 'catalog/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ContactsView(TemplateView):
    """
    Class-based view for displaying the contacts page
    """
    template_name = 'catalog/contacts.html'


class ProductDetailView(TemplateView):
    template_name = 'catalog/product_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=kwargs['pk'])
        return context
