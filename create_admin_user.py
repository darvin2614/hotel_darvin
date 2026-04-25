from django.contrib.auth.models import User

# Create admin user if not exists
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@hotel.com',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Admin',
        'last_name': 'User'
    }
)

if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print('✓ Created admin user: admin@hotel.com / admin123')
else:
    print('✓ Admin user already exists')
    # Reset password to admin123
    admin_user.set_password('admin123')
    admin_user.save()
    print('✓ Reset admin password to: admin123')

print(f'Admin user ID: {admin_user.id}')
print(f'Admin user email: {admin_user.email}')
print(f'Admin user is_superuser: {admin_user.is_superuser}')
