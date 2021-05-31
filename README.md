# Commandes de base 
## Run
Pour exécuter l'application, docker et docker-compose doivent être installés sur votre système. Pour les instructions d'installation, reportez-vous à la [documentation Docker]( https://docs.docker.com/compose/install/ ).

L'application doit être construite avant d'être lancée :

`docker-compose -f docker-compose.dev.yml build`

Une fois construite, vous pouvez démarrer les containers :

`docker-compose -f docker-compose.dev.yml up -d`

L'option -d permet de lancer les containers en arrière tâche. 

## Accéder à la liste des conteneurs en cours d'utilisation 
Il peut être utile d'accéder au shell des containers, pour créer un utilisateur, lire des tables de la BDD, vérifier une configuration de NGINX, ...
Pour cela, il faut récupérer l'identifiant du container via :

`docker ps`

Voici un exemple de mes containers lancés :

```
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                    NAMES
ef8021bfb8c0   ontable_proxy           "/docker-entrypoint.…"   13 minutes ago   Up 10 minutes   0.0.0.0:80->80/tcp       proxy
a4ba950d5eee   ontable_backend         "/home/app/web/entry…"   13 minutes ago   Up 10 minutes   8000/tcp                 backend
499245507d18   postgres11-postgis2.5   "docker-entrypoint.s…"   18 minutes ago   Up 10 minutes   0.0.0.0:5432->5432/tcp   postgres11-postgis2.5
```

### RUN FAST
Pour les pressés :
`docker-compose -f docker-compose.dev.yml up --build -d`

---
## Créer un super utilisateur django (ontable_backend)
Une fois l'identifiant obtenu ( via `docker ps`), on accède au terminal du container de l'image ontable_backend. C'est cette image qui gère Django, l'API et la partie restaurateur. 

`docker exec -it  8ccc0f8dff96 bash`

Le repertoire de l'application se trouve dans /home/app/web/. On accède donc au fichier manage.py afin de pouvoir créer un superutilisateur. 

`python /home/app/web/manage.py createsuperuser`

## Accéder à la base de données :
On repète le même principe pour accéder à la BDD ou bien à NGINX. 
Ici, on utilise non pas bash, mais psql, l'interface en mode texte pour PostgresSQL. Il permet de saisir des requêtes de façon interractive. 

On accède au container, à la BDD onTable. En developpment, aucun mot de passe n'est requis.  
`docker exec -it 499245507d18 psql -U user -d onTable -W `

## Acceder au container de redis 

`docker exec -it 566c3b041e62 redis-cli`

## Accéder à la configuration d'un container 

`docker inspect name_container`

## Afficher la liste des tables de la BDD
`\dt`

## Accéder à Nginx/Alpine ou à sa configuration 
On accède au container NGINX via /bin/ash ( aucune idée de pourquoi ils utilisent Almquist shell )
`docker exec -it 86ab91f5e010 /bin/ash`

## Nettoyer docker :

`docker system prune`
___

# Configuration Docker 
Les fichiers de composition Docker permettent de spécifier des configurations complexes de plusieurs services interdépendants à exécuter ensemble en tant que cluster de conteneurs Docker. Consultez l'excellente référence de docker-compose pour en savoir plus sur les nombreux paramètres configurables. Les fichiers de composition sont écrits au format .yml et comportent trois clés de niveau supérieur: services, volumes et réseaux. Chaque service de la section services définit un conteneur Docker distinct avec une configuration indépendante des autres services.

Pour prendre en charge plusieurs environnements, plusieurs fichiers docker-compose sont utilisés dans ce projet. 
docker-compose.prod.yml pour la configuration des containers lors de la production avec AWS ou bien Raspberry 
docker-compose.dev.yml pour la configuration des containers lors de la phase de développement

## Les services
OnTable est composé de plusieurs services :
`backend` : composant central de l'application Django chargé de traiter les demandes des utilisateurs
`frontend`: Programmé en vue.js, il est envoyé au client lorsqu'il demande /orders/ ou bien la page d'accueil. 
`db`: fournit la base de données Postgres 
`redis`: agit comme un courtier de messages, distribuant les tâches sous forme de messages de l'application aux ouvriers de celery
`celery_beat`et `celery_worker`: gèrent respectivement la planification des tâches périodiques et l'exécution asynchrone des tâches définies par l'application Django
`proxy` : agit en tant que proxy pour l'application, il gère le routage en redirigeant les requêtes via les différents services. En production, Nginx doit être utilisé comme serveur Web pour l'application, transmettant les demandes à gunicorn qui à son tour interagit avec l'application via l'interface de passerelle de serveur Web ( WSGI : `/backend/onTableAPI/wsgi.py`) de l'application

## Les réseaux 
La différence entre `port` et `expose` est simple :
`expose`expose les ports uniquement aux services liés sur le même réseau
`ports` expose les ports à la fois aux services liés sur le même réseau et à la machine hôte (soit sur un port hôte aléatoire, soit sur un port hôte spécifique si spécifié).

Remarque : lorsque vous utilisez les touches expose ou ports, spécifiez toujours les ports en utilisant des chaînes entre guillemets, car les ports spécifiés sous forme de nombres peuvent être interprétés de manière incorrecte lorsque le fichier de composition est analysé et donner des résultats inattendus.

## Les Volumes 
A compléter

# Mise en production 
## Configurer le docker-compose :
en production dans le fichier conf/.env.prod
en development dans le fichier conf/.env.dev
pour le backend, la Liste des variables à configurer est dans le fichier app/appName/settings.common.py

## Avant la prod : 
- Scanner les images pour trouver des vulnérablités avec : docker scan [IMAGE]
- Adapter le dockerfile du frontend 
- Système de backups auto 


## Programmation :
- API à finir 
- Mettre en place la séparation entre le compte entreprise et la partie order/présentation de l'entreprise
- https://medium.com/@magyarn/building-an-online-store-with-vue-cli-part-4-612d99230f92
- https://medium.com/swlh/searching-in-django-rest-framework-45aad62e7782
- https://www.digitalocean.com/community/tutorials/how-to-navigate-between-views-with-vue-router


## Configurer le serveur :
Empecher les pings : 
modifier les ports SSH
Port 80 à laisser sur un port standard
Pare-feu à gérer 


### NGINX configuration : 

#### Test Nginx configuration

`service nginx configtest`

#### Check Nginx version

`service nginx -V`

#### View server status

`service nginx status`

#### Reload Nginx

`service nginx reload`

#### Start, Stop, Restart Nginx

`service nginx start`

`service nginx stop`

`service nginx reload`


Enlever la version de nginx : 
https://www.tecmint.com/hide-nginx-server-version-in-linux/

___ 
# Github Commands 
## fetch the changes from the remote
git fetch origin

## show commit logs of changes
git log master..origin/master

## show diffs of changes
git diff master..origin/master

## apply the changes by merge..
git merge origin/master

## .. or just pull the changes
git pull

___

# Redis & Celery 
Pour s'assurer que l'application Django ne se bloque pas en raison de l'exécution en série de longue tâches, 
des ouvriers celery sont utilisés. Celery fournit un pool de processus de travail vers lesquels les tâches lourdes ou longues du processeur peuvent être différées sous la forme de tâches asynchrones 

L'application Celery doit être définie dans `/backend/onTableAPI/settings/celery.py`, paramétrée pour obtenir la configuration à partir de la configuration Django et pour découvrir automatiquement les tâches définies tout au long du projet Django.

La base de données de l'application Django, c'est-à-dire le service `postgres`, sera utilisée comme backend des résultats Celery. Les tâches périodiques à planifier par le `celery_beat` service sont également définies ici. 

Redis est un broker, une file d'attente, il stocke les tâches.

Links :
- Celery / Redis : https://testdriven.io/blog/django-celery-periodic-tasks/
- https://soshace.com/dockerizing-django-with-postgres-redis-and-celery/
- https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose



# Security 

## Utiliser des outils sécurisés
Enlever les packages qui sont pas sécurisés
`sudo apt-get --purge remove xinetd nis yp-tools tftpd atftpd tftpd-hpa telnetd rsh-server rsh-redone-server`


## Fail2Ban 
Contre les brutes force de bots ou d'utilisateurs 

Fail2ban est une application qui analyse les logs de divers services (SSH, Apache, FTP…) en cherchant des correspondances entre des motifs définis dans ses filtres et les entrées des logs. Lorsqu'une correspondance est trouvée, une ou plusieurs actions sont exécutées. Fail2ban cherche des tentatives répétées de connexions infructueuses dans les fichiers journaux et procède à un bannissement en ajoutant une règle au pare-feu pour bannir l'adresse IP de la source.

Installer fail2Ban : `sudo apt install fail2ban`

Quelques liens : 
https://www.julienmousqueton.fr/fail2ban-pour-nginx/

https://buzut.net/installer-et-parametrer-fail2ban/

## SELinux 
SELinux (Security Enhanced Linux) est un système de contrôle d'accès obligatoire (Mandatory Access Control).Concrètement, le noyau interroge SELinux avant chaque appel système pour savoir si le processus est autorisé à effectuer l'opération concernée.

SELinux s'appuie sur un ensemble de règles (policy) pour autoriser ou interdire une opération. Ces règles sont assez délicates à créer, mais heureusement deux jeux de règles standards (targeted et strict) sont fournies pour éviter le plus gros du travail de configuration.

Installation : `apt install selinux-basics selinux-policy-default`

