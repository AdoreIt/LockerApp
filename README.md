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


### RabbitQM  Setup<a name="rabbitmq"></a>

To configure hostname, edit `hosts`

`sudo vim /etc/hosts`

Add to file:
```
xxx.xxx.xxx.xxx rabbit01
xxx.xxx.xxx.xxx rabbit02
```
where `xxx.xxx.xxx.xxx` is ip addresses where the nodes will be launched, `rabbit01` and `rabbit02` are node names.

Create file `rabbitmq-env.conf` with the next line:
```
rabbit01$ vim conda/envs/env_name/etc/rabbitmq-env.conf
NODENAME=rabbit@rabbit01

rabbit02$ vim conda/envs/env_name/etc/rabbitmq-env.conf
NODENAME=rabbit@rabbit02
```

`rabbit01$` is one computer, `rabbit02$` is another computer.

Start independent nodes: run `rabbitmq-server` on each computer:
```
rabbit01$ rabbitmq-server
rabbit02$ rabbitmq-server
```

This creates two independent RabbitMQ brokers, one on each node, as confirmed by the `cluster_status` command:
```
rabbit01$ rabbitmqctl cluster_status
Cluster status of node rabbit@rabbit01 ...
[{nodes,[{disc,[rabbit@rabbit01]}]},{running_nodes,[rabbit@rabbit01]}]
...done.

rabbit02$ rabbitmqctl cluster_status
Cluster status of node rabbit@rabbit02 ...
[{nodes,[{disc,[rabbit@rabbit02]}]},{running_nodes,[rabbit@rabbit02]}]
...done.
```

Create the cluster
```
rabbit02$ rabbitmqctl stop_app
Stopping node rabbit@rabbit02 ...done.

rabbit02$ rabbitmqctl join_cluster rabbit@rabbit01
Clustering node rabbit@rabbit02 with [rabbit@rabbit01] ...done.

rabbit02$ rabbitmqctl start_app
Starting node rabbit@rabbit02 ...done.
```

We can see that the two nodes are joined in a cluster by running the `cluster_status` command on either of the nodes:
```
rabbit01$ rabbitmqctl cluster_status
Cluster status of node rabbit@rabbit1 ...
[{nodes,[{disc,[rabbit@rabbit01,rabbit@rabbit02]}]},
{running_nodes,[rabbit@rabbit02,rabbit@rabbit01]}]
...done.
```

## Launching  <a name="launching"></a>
Launch LockerApp:

`python locker_app/app.py`

Launch LockerService:

`python locker_service/locker_service.py`

Launch UserService:

`python user_service/user_service.py`

Launch RabbitMQ cluster (two nodes from different computers whose ip adresses are specified in `/etc/hosts`):
```
rabbit01$ rabbitmq-server

rabbit02$ rabbitmq-server
```

Launch RabbitMQ receiver for LockerService:

`python locker_service/rabbitmq_receive_from_user_service.py`
