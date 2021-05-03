# thanks to https://fr.vuejs.org/v2/cookbook/dockerize-vuejs-app.html
# dev mode
FROM node:10-alpine as builder

# définit le dossier 'frontend' comme dossier de travail
WORKDIR /frontend

# copie 'package.json' et 'package-lock.json' (si disponible)
COPY package*.json ./

# installe les dépendances du projet
RUN npm install

# copie les fichiers et dossiers du projet dans le dossier frontend
COPY . .

# construit l'app pour la production en la minifiant
RUN npm run build 

# Copy from volume of frontend PROBLEME ICI
COPY . frontend_src:/home/app/frontend/src

# installe un simple serveur http pour servir un contenu statique
RUN npm install -g http-server

