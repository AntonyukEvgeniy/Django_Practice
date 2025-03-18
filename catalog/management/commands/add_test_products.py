from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal
class Command(BaseCommand):
    help = 'Добавить тестовые продукты в БД'
    def handle(self, *args, **options):
        # Удаляем существующие данные
        self.stdout.write('Deleting existing data...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        # Создаем тестовые категории
        self.stdout.write('Creating test categories...')
        categories = {
            'Электроника': 'Электронные устройства и гаджеты',
            'Одежда': 'Мужская и женская одежда',
            'Книги': 'Художественная и учебная литература'
        }
        created_categories = {}
        for name, description in categories.items():
            category = Category.objects.create(
                name=name,
                description=description
            )
            created_categories[name] = category
            self.stdout.write(f'Created category: {name}')
        # Создаем тестовые продукты
        self.stdout.write('Creating test products...')
        products = [
            {
                'name': 'Смартфон XPhone',
                'description': 'Современный смартфон с отличной камерой',
                'category': 'Электроника',
                'purchase_price': '29999.99'
            },
            {
                'name': 'Джинсы Classic',
                'description': 'Классические джинсы синего цвета',
                'category': 'Одежда',
                'purchase_price': '2999.99'
            },
            {
                'name': 'Python для начинающих',
                'description': 'Лучшая книга для изучения Python',
                'category': 'Книги',
                'purchase_price': '999.99'
            }
        ]
        for product_data in products:
            category = created_categories[product_data['category']]
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                category=category,
                purchase_price=Decimal(product_data['purchase_price'])
            )
            self.stdout.write(f'Created product: {product.name}')
        self.stdout.write(self.style.SUCCESS('Successfully added test data'))