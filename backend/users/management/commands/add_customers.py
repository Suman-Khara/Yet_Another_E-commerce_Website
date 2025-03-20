import random
from django.contrib.auth.models import User
from users.models import Customer

def generate_random_phone_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def generate_random_address():
    addresses = [
        "123 Elm St, Springfield", "456 Oak Ave, Lincoln", "789 Maple Dr, Austin",
        "101 Pine Rd, Denver", "202 Birch Ln, Seattle", "303 Cedar Blvd, Boston"
    ]
    return random.choice(addresses)

def create_customers_from_file(file_path='reviewers.txt'):
    with open(file_path, 'r') as file:
        for line in file:
            name, email = line.strip().split(',')
            username = name.lower().replace(' ', '')
            password = username

            # Create user
            user, created = User.objects.get_or_create(username=username, email=email.strip())
            if created:
                user.set_password(password)
                user.save()

                # Create customer
                Customer.objects.create(
                    user=user,
                    phone_number=generate_random_phone_number(),
                    address=generate_random_address(),
                    verified=True
                )
                print(f"Customer created: {username}")
            else:
                print(f"User with username '{username}' already exists.")

create_customers_from_file()