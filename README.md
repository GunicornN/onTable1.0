# Configurer le système :
en production dans le fichier conf/.env.dev
en development dans le fichier conf/.env.prod
la Liste des variables à configurer est dans le fichier app/appName/settings.common.py


# Create superuser :
`docker ps`
`docker exec -it  8ccc0f8dff96 bash`
`python /home/app/web/manage.py createsuperuser`
