from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    """
    Контроллер для главной страницы
    """
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


def contacts(request):
    """
    Контроллер для страницы контактов
    """
    return render(request, "catalog/contacts.html")


def product_detail(request, pk):
    """
    Отображение детальной информации о продукте
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})
