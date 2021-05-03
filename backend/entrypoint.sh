#!/bin/sh

echo "PostgreSQL started"

# scripts 
cd $APP_HOME

python manage.py makemigrations 
python manage.py migrate
python manage.py collectstatic --noinput

# init db 
python manage.py loaddata types
python manage.py init_companies

# Start the server w/ gunicorn wsgi
gunicorn onTableAPI.wsgi:application --bind 0.0.0.0:8000
