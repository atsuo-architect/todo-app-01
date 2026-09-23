#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell -c '
from django.db import connection

tables = connection.introspection.table_names()

print("=== DATABASE TABLES ===")
for table in sorted(tables):
    print(table)

print("=== END ===")
'

python manage.py shell -c '
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_ADMIN_USERNAME")
email = os.getenv("DJANGO_ADMIN_EMAIL", "")
password = os.getenv("DJANGO_ADMIN_PASSWORD")

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print(f"Created superuser: {username}")
else:
    print("Superuser already exists or credentials are not configured.")
'

python manage.py shell -c '
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

print("=== USER COUNT ===")
print(User.objects.count())

print("=== SUPERUSER COUNT ===")
print(User.objects.filter(is_superuser=True).count())

print("=== DATABASE NAME ===")
print(connection.settings_dict.get("NAME"))

print("=== DATABASE HOST ===")
print(connection.settings_dict.get("HOST"))

print("=== END USER CHECK ===")
'

python manage.py shell -c '
from django.contrib.auth import get_user_model

User = get_user_model()

print("=== USER QUERY TEST ===")

for user in User.objects.all():
    print(
        user.username,
        user.is_staff,
        user.is_superuser,
        user.is_active
    )

print("=== END USER QUERY TEST ===")
'