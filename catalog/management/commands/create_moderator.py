from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from catalog.models import Product
from users.models import CustomUser


class Command(BaseCommand):
    help = "Creates a moderator user and adds them to Product Moderator group"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email for the moderator")
        parser.add_argument("username", type=str, help="Username for the moderator")
        parser.add_argument("password", type=str, help="Password for the moderator")

    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        try:
            # Create the user
            user = CustomUser.objects.create_user(
                email=email, username=username, password=password
            )
            # Add user to Product Moderator group
            moderator_group, created = Group.objects.get_or_create(
                name="Product Moderator"
            )
            # Get content type for Product model
            product_content_type = ContentType.objects.get_for_model(Product)
            # Get permissions
            view_product = Permission.objects.get(
                codename="view_product", content_type=product_content_type
            )
            add_product = Permission.objects.get(
                codename="add_product", content_type=product_content_type
            )
            change_product = Permission.objects.get(
                codename="change_product", content_type=product_content_type
            )
            delete_product = Permission.objects.get(
                codename="delete_product", content_type=product_content_type
            )
            can_unpublish_product = Permission.objects.get(
                codename="can_unpublish_product", content_type=product_content_type
            )
            # Assign permissions to group
            moderator_group.permissions.add(
                view_product,
                add_product,
                change_product,
                delete_product,
                can_unpublish_product,
            )
            user.groups.add(moderator_group)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created moderator user: {username}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating moderator: {str(e)}"))
