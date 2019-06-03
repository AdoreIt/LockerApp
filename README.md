# LokerApp

![](https://github.com/AdoreIt/LockerApp/blob/master/doc/LockerApp.gif?raw=true)

- [LokerApp](#lokerapp)
  - [Basic architecture](#basic-architecture)
  - [Installs](#installs)
    - [Conda environment](#conda-environment)
    - [Databases installation, configuration and creation](#databases-installation-configuration-and-creation)
      - [PostgreSQL](#postgresql)
        - [Install PostgreSQL on Ubuntu](#install-postgresql-on-ubuntu)
        - [Start PostgreSQL server](#start-postgresql-server)
        - [Create Database](#create-database)
        - [Drop Database](#drop-database)
      - [MongoDB](#mongodb)
        - [Install python lib](#install-python-lib)
        - [Create database folders](#create-database-folders)
        - [Create Database](#create-database-1)
        - [Drop Database](#drop-database-1)
    - [RabbitQM Setup](#rabbitqm-setup)
  - [Launching](#launching)
    - [If you have troubles with creating replica set, run](#if-you-have-troubles-with-creating-replica-set-run)
    - [Launching with Guake terminal](#launching-with-guake-terminal)

## Basic architecture

![](https://github.com/AdoreIt/LockerApp/blob/master/doc/architecture_diagram.png?raw=true)

## Installs
### Conda environment

Create an environment and activate it

``` bash
conda create --name p36_lockerapp python=3.6
conda activate p36_lockerapp
```

Flask and RestAPI

``` bash
pip install flask
pip install flask-restful
```

RabbitMQ

``` bash
conda install -c conda-forge rabbitmq-server
conda install -c conda-forge pika
conda install -c conda-forge colorlog
```

Postgresql

``` bash
conda install -c anaconda psycopg2
```

HAProxy
``` bash
conda install -c bkreider haproxy
```

### Databases installation, configuration and creation

#### PostgreSQL

##### Install PostgreSQL on Ubuntu

``` bash
sudo apt update
sudo apt-get install postgresql postgresql-contrib
# optionally:
sudo apt-get install libpq-dev postgresql-client postgresql-client-common
```

<details>
  <summary>If you not using conda</summary>
  
Install python lib (can be succesfully executed only if PostgreSQL is already installed):

``` bash
pip install psycopg2
```

</details>

##### Start PostgreSQL server

(Required before running the app):

``` bash
sudo service postgresql start
```

##### Create Database

``` bash
psql -f create_users_db.sql -U postgres \
&& psql -f create_users_table.sql -U postgres -d users_db
```

##### Drop Database

``` bash
psql -f drop_users_db.sql -U postgres
```

#### MongoDB

<details>
  <summary> Install MongoDB on Ubuntu if you don't use Conda </summary>

``` bash
sudo apt update
sudo apt install -y mongodb
```

##### Install python lib

```bash
python -m pip install pymongo
```

</details>

##### Create database folders

```bash
cd mongo_db
mkdir db0 db1 db2
```

##### Create Database

```bash
python locker_service/mongo_db/migrations/create_lockers_db.py
```

##### Drop Database

```bash
python locker_service/mongo_db/migrations/drop_mongo_db.py`
```

### RabbitQM  Setup

To configure hostname, edit `hosts`

``` bash
sudo vim /etc/hosts
```

Add to file:

``` text
xxx.xxx.xxx.xxx rabbit01
xxx.xxx.xxx.xxx rabbit02
```

where `xxx.xxx.xxx.xxx` is ip addresses where the nodes will be launched, `rabbit01` and `rabbit02` are node names.

Create file `rabbitmq-env.conf` with the next line:

`rabbit01$ vim ~/anaconda3/envs/p36_lockerapp/etc/rabbitmq-env.conf`
>NODENAME=rabbit@rabbit01

`rabbit02$ vim ~/anaconda3/envs/p36_lockerapp/etc/rabbitmq-env.conf`
>NODENAME=rabbit@rabbit02

`rabbit01$` is one computer, `rabbit02$` is another computer.

Start independent nodes: run `rabbitmq-server` on each computer:

``` bash
rabbit01$ rabbitmq-server
rabbit02$ rabbitmq-server
```

This creates two independent RabbitMQ brokers, one on each node, as confirmed by the `cluster_status` command:

`rabbit01$ rabbitmqctl cluster_status`
>Cluster status of node rabbit@rabbit01 ...
[{nodes,[{disc,[rabbit@rabbit01]}]},{running_nodes,[rabbit@rabbit01]}]
...done.

`rabbit02$ rabbitmqctl cluster_status`
>Cluster status of node rabbit@rabbit02 ...
[{nodes,[{disc,[rabbit@rabbit02]}]},{running_nodes,[rabbit@rabbit02]}]
...done.

Create the cluster

`rabbit02$ rabbitmqctl stop_app`
>Stopping node rabbit@rabbit02 ...done.

`rabbit02$ rabbitmqctl join_cluster rabbit@rabbit01`
>Clustering node rabbit@rabbit02 with [rabbit@rabbit01] ...done.

`rabbit02$ rabbitmqctl start_app`
>Starting node rabbit@rabbit02 ...done.

We can see that the two nodes are joined in a cluster by running the `cluster_status` command on either of the nodes:

`rabbit01$ rabbitmqctl cluster_status`
>Cluster status of node rabbit@rabbit1 ...
[{nodes,[{disc,[rabbit@rabbit01,rabbit@rabbit02]}]},
{running_nodes,[rabbit@rabbit02,rabbit@rabbit01]}]
...done.

Enable `rabbitmq_management` in every node

`rabbitmq-plugins enable rabbitmq_management`

Create admin user on one node, this admin user can be used for any node in cluster

``` bash
rabbitmqctl add_user <user> <password>
rabbitmqctl set_user_tags <user> administrator
rabbitmqctl set_permissions -p / <user> ".*" ".*" ".*"
```

(or set permissions through management website `xxx.xxx.xxx.xxx:15672`)

## Launching

Update `config/config.json` with

- ip and host information of services
- credentials for RabbitMQ user

Launch **HAProxy**

```bash
(p36_lockerapp)$ haproxy -f config/haproxy.cfg
```

Launch **LockerApp** from two computers (don't forget to have different LockerApp ip in `config/config.json` — they are also written in `config/haproxy.cfg`):

`(p36_lockerapp)$ python locker_app/app.py`

Launch **LockerService**:

`(p36_lockerapp)$ python locker_service/locker_service.py`

Launch **UserService**:

`(p36_lockerapp)$ python user_service/user_service.py`

Launch **RabbitMQ cluster** (two nodes from different computers whose ip adresses are specified in `/etc/hosts`):

``` bash
rabbit01$ rabbitmq-server

rabbit02$ rabbitmq-server
```

Launch **RabbitMQ receiver** for LockerService:

``` bash
(p36_lockerapp)$ python locker_service/rabbitmq_receive_from_user_service.py
```

Launch **MongoDB** with replication: run three separate mongodb servers

```bash
(p36_lockerapp)$ mongod --port 27017 --dbpath ./db0 --replSet lockers_rs
(p36_lockerapp)$ mongod --port 27018 --dbpath ./db1 --replSet lockers_rs
(p36_lockerapp)$ mongod --port 27019 --dbpath ./db2 --replSet lockers_rs
```

Initialize replica set

``` bash
(p36_lockerapp)$ python locker_service/mongo_db/migrations/create_lockers_db.py
```

### If you have troubles with creating replica set, run

``` bash
(p36_lockerapp)$ mongod --port 27017 --dbpath ./db0 --replSet lockers_rs
```

In another terminal run `mongo` to open MongoDB terminal (when only one mongo node is active).
Then run `rs.init()`, launch other nodes

``` bash
(p36_lockerapp)$ mongod --port 27018 --dbpath ./db1 --replSet lockers_rs
(p36_lockerapp)$ mongod --port 27019 --dbpath ./db2 --replSet lockers_rs
```

and add these two members to the replica set by executing

``` bash
(p36_lockerapp)$ rs.add("localhost:27018");
(p36_lockerapp)$ rs.add("localhost:27019");
```

Then run

``` bash
(p36_lockerapp)$ python locker_service/mongo_db/migrations/create_lockers_db.py
```

without command

```` bash
(p36_lockerapp)$ python locker_service/mongo_db/migrations/create_lockers_db.py
````

### Launching with Guake terminal

From LockerApp folder:

``` bash
# to run LockerApp, LockerService, 3 mongos, Hazelcast and RabbitMQ
./scripts/locker_app_run.sh

# to run LockerApp(second instance), UserService, Hazelcast and RabbitMQ
./scripts/user_service_run.sh
```
