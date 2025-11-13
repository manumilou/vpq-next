#!/usr/bin/env python
"""
Quick script to create a superuser on Railway.
Run with: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'victimes_pesticides.settings.railway')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'manu'
email = 'manu@example.com'
password = 'temppassword123'  # Change this after first login

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
    user = User.objects.get(username=username)
    print(f"Resetting password for '{username}'...")
    user.set_password(password)
    user.save()
    print(f"Password reset successfully!")
else:
    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser created successfully!")

print(f"\nLogin with:")
print(f"  Username: {username}")
print(f"  Password: {password}")
print(f"\nPlease change the password after logging in!")
