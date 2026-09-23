#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

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