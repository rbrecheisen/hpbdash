#!/bin/bash

cd src/hpbdash/app/migrations
rm -r *
touch __init__.py

cd ../..

rm db.sqlite3

python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell
echo "Successfully created super user \"admin\""

python manage.py runserver