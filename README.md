# cv_masters_lockers
Distributed system project

1. [Basic architecture](#architecture)

## Basic architecture <a name="architecture"></a>
![](https://github.com/AdoreIt/cv_masters_lockers/blob/master/doc/architecture_diagram.png?raw=true)

## Databases installation, configuration and creation

#### PostgreSQL

##### Install PostgreSQL on Ubuntu:
`sudo apt update`

`sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common`

##### Install python lib (can be succesfully executed only if PostgreSQL is already installed):
`pip install psycopg2`

##### Start PostgreSQL server (Required before running the app):
`sudo service postgresql start`

##### Create Database:
`cd dbs && ./create_psql_db.sh`

##### Drop Database
`cd dbs && ./drop_psql_db.sh`

#### MongoDB

##### Install MongoDB on Ubuntu:
`sudo apt update`

`sudo apt install -y mongodb`

##### Install python lib:
`python -m pip install pymongo`

##### Start MongoDB server:
`sudo service mongodb start`

##### Create Database
`cd dbs && bash create_mongo_db.sh`

##### Drop Database
`cd dbs && bash drop_mongo_db.sh`