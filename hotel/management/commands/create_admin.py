from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create admin user for the hotel management system'

    def handle(self, *args, **options):
        try:
            # Check if admin user already exists
            if User.objects.filter(email='admin@hotel.com').exists():
                self.stdout.write(
                    self.style.SUCCESS('Admin user already exists.')
                )
                return

            # Create admin user
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@hotel.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            
            self.stdout.write(
                self.style.SUCCESS('Admin user created successfully.')
            )
            self.stdout.write(
                self.style.SUCCESS('Email: admin@hotel.com')
            )
            self.stdout.write(
                self.style.SUCCESS('Password: admin123')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )
