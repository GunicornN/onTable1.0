# DataBase 

## Create Database for production 
docker run --name=postgis -d -e POSTGRES_USER=user -e POSTGRES_PASS=password -e POSTGRES_DBNAME=onTable -p 5432:5432 kartoza/postgis:9.6-2.4

