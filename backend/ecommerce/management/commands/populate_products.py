import json
from datetime import datetime
from django.core.management.base import BaseCommand
from ecommerce.models import Category, Product, Tag, Review, Seller, Customer
from users.models import User

class Command(BaseCommand):
    help = 'Populate database with products and reviews from products.json'

    def handle(self, *args, **kwargs):
        try:
            with open('products.json', 'r') as file:
                data = json.load(file)

            abc_store, _ = Seller.objects.get_or_create(store_name='ABC_Store')
            xyz_shop, _ = Seller.objects.get_or_create(store_name='XYZ_Shop')
            random_shop, _ = Seller.objects.get_or_create(store_name='Random')

            for idx, item in enumerate(data.get('products', [])):
                # Create or get category
                category, _ = Category.objects.get_or_create(name=item['category'])

                # Create or get tags
                tags = []
                for tag_name in item.get('tags', []):
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    tags.append(tag)

                # Determine seller
                seller = abc_store if idx < 10 else xyz_shop if idx < 20 else random_shop

                # Create product
                product = Product.objects.create(
                    product_id=item['id'],
                    seller=seller,
                    name=item['title'],
                    description=item.get('description', ''),
                    price=item['price'],
                    stock=item['stock'],
                    category=category,
                    discount=item.get('discountPercentage', 0.0),
                    rating=item.get('rating', 0.0),
                    image_url=item['images'][0] if item.get('images') else None,
                    thumbnail_url=item.get('thumbnail')
                )

                product.tags.set(tags)
                product.save()

                # Create reviews
                for review_data in item.get('reviews', []):
                    user, _ = User.objects.get_or_create(email=review_data['reviewerEmail'], defaults={'username': review_data['reviewerName']})
                    customer, _ = Customer.objects.get_or_create(user=user)
                    Review.objects.create(
                        product=product,
                        user=customer,
                        rating=review_data['rating'],
                        comment=review_data.get('comment', ''),
                        created_at=datetime.fromisoformat(review_data['date'].replace('Z', '+00:00'))
                    )

            self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))