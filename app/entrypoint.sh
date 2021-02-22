#!/bin/sh



echo "PostgreSQL started"


# scripts 
cd $APP_HOME

python manage.py flush --no-input
python manage.py makemigrations 
python manage.py migrate
sudo python manage.py collectstatic --noinput


# Start the server w/ gunicorn wsgi
gunicorn onTableAPI.wsgi:application --bind 0.0.0.0:8000