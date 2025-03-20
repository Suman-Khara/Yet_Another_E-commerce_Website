import json
from django.core.management.base import BaseCommand
from ecommerce.models import *

class Command(BaseCommand):
    help = 'Import products and reviews from products.json and update the database.'

    def handle(self, *args, **kwargs):
        try:
            # Load JSON data
            with open('ecommerce/products.json', 'r') as file:
                data = json.load(file)

            # Pre-fetch sellers
            abc_store, _ = Seller.objects.get_or_create(store_name='ABC_Store')
            xyz_shop, _ = Seller.objects.get_or_create(store_name='XYZ_Shop')
            random_shop, _ = Seller.objects.get_or_create(store_name='Random')

            for idx, item in enumerate(data['products']):
                # Assign seller based on index
                seller = abc_store if idx < 10 else xyz_shop if idx < 20 else random_shop

                # Get category or create if not found
                category, _ = Category.objects.get_or_create(name=item.get('category', 'Uncategorized'))

                # Create or update Product
                product, created = Product.objects.update_or_create(
                    product_id=item['id'],
                    defaults={
                        'seller': seller,
                        'name': item['title'],
                        'description': item['description'],
                        'price': item['price'],
                        'stock': item['stock'],
                        'category': category,
                        'discount': item.get('discountPercentage', 0.00),
                        'rating': item['rating'],
                        'total_reviews': len(item['reviews']),
                        'image_url': item['images'][0] if item['images'] else None,
                        'thumbnail_url': item.get('thumbnail', None),
                    }
                )

                # Manage Tags
                product.tags.clear()
                for tag_name in item.get('tags', []):
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    product.tags.add(tag)

                # Create Reviews
                print(f'Processing product: {product.name} with number of reviews = {len(item["reviews"])}')
                for review_data in item['reviews']:
                    user, _ = User.objects.get_or_create(email=review_data['reviewerEmail'], defaults={'username': review_data['reviewerName']})
                    customer, _ = Customer.objects.get_or_create(user=user)
                    Review.objects.update_or_create(
                        product=product,
                        user=customer,
                        defaults={
                            'rating': review_data['rating'],
                            'comment': review_data['comment'],
                        }
                    )

                self.stdout.write(self.style.SUCCESS(f"Processed product: {product.name}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))
