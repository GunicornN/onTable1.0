# Documentation for users API 

## Create superuser :
python manage.py createsuperuser

## Generate a token
python manage.py drf_create_token vitor


https://django-rest-auth.readthedocs.io/en/latest/faq.html

## Login 
(POST) http://127.0.0.1:8000/rest-auth/login/ 

Body Params :
username
email
password

Returns Token key

## Logout 
(POST) /rest-auth/logout/ 


## Reset Password
(POST) /rest-auth/password/reset/ 

Body Params :
email

## Registration

(POST) /rest-auth/registration/ 

Body Params :
username
password1
password2
email
