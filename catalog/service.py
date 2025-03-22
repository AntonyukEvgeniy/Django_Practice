from catalog.models import Product


def get_products_by_category(category_id, user=None):
    """
    Возвращает список продуктов для указанной категории.
    Если пользователь является модератором, возвращаются все продукты,
    иначе только опубликованные.
    """
    queryset = Product.objects.filter(category_id=category_id)
    if user and user.groups.filter(name="Product Moderator").exists():
        return queryset
    return queryset.filter(is_published=True)
