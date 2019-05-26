# cv_masters_lockers
Distributed system project

![](https://github.com/AdoreIt/LockerApp/blob/master/doc/LockerApp.gif?raw=true)

1. [Basic architecture](#architecture)
2. [Installs](#installs)
   1. [Conda enviroment](#conda_environment)
   2. [Databases](#databases)
      1. [PostgreSQL](#postgresql)
      2. [MongoDB](#mongodb)
   3. [RabbitMQ](#rabbitmq)
3. [Launching](#launching)


## Basic architecture <a name="architecture"></a>
![](https://github.com/AdoreIt/LockerApp/blob/master/doc/architecture_diagram.png?raw=true)

## Installs  <a name="installs"></a>
### Conda environment  <a name="conda_environment"></a>

Create an environment and activate it
```
conda create --name p36_lockerapp python=3.6
conda activate p36_lockerapp
```

Flask and RestAPI
```
pip install flask
pip install flask-restful
```

RabbitMQ
```
conda install -c conda-forge rabbitmq-server
conda install -c conda-forge pika
```

### Databases installation, configuration and creation <a name="databases"></a>

#### PostgreSQL <a name="postgresql"></a>

Install PostgreSQL on Ubuntu:
```
sudo apt update
sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
```

Install python lib (can be succesfully executed only if PostgreSQL is already installed):

`pip install psycopg2`

Start PostgreSQL server (Required before running the app):

`sudo service postgresql start`

Create Database:

`cd user_service/psql_db && ./create_psql_db.sh`

Drop Database:

`cd user_service/psql_db && ./drop_psql_db.sh`


#### MongoDB <a name="mongodb"></a>

Install MongoDB on Ubuntu:
```
sudo apt update
sudo apt install -y mongodb
```

Install python lib:

`python -m pip install pymongo`

Start MongoDB server:

`sudo service mongodb start`

Create Database:

`cd locker_service/mongo_db && bash create_mongo_db.sh`

Drop Database:

`cd locker_service/mongo_db && bash drop_mongo_db.sh`


### RabbitQM  <a name="rabbitmq"></a>

## Launching  <a name="launching"></a>
