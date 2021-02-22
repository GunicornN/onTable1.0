FROM python:3.8-slim

# set work directory
WORKDIR /usr/src/app

## Install depencies 
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

## GDAL for spatial db 
RUN apt-get update
RUN apt-get --assume-yes install libgdal-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

#Install netcat 
RUN apt install -y netcat

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## Static
# create the app user
# RUN groupadd app &&
RUN   useradd -m -p p00am2ze1hekaaj7181 app


ENV HOME=/home/app
ENV APP_HOME=/home/app/web

# Create web app directory 
RUN mkdir -p $APP_HOME

# STATIC files inside docker image 
RUN mkdir -p $APP_HOME/staticfiles

## Entrypoint 
# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user (-Recursive)
RUN chown -R app $APP_HOME
RUN chown -R app /home/app/web/

# change to the app user
USER app

## Connexion between Django and the DB
# it run this script when docker up
ENTRYPOINT ["/home/app/web/entrypoint.sh"]  

