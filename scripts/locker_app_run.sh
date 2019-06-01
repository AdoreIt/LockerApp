#!/bin/sh

# chmod +x locker_app_run.sh

# change ... to your path
locker_app_path="$HOME/.../LockerApp"
# change env_name to your env name
anaconda_env_activate="conda activate env_name"

# create locker tab
guake --new-tab $locker_app_path -r "LockerApp" -e "$anaconda_env_activate  && clear"
guake -e "python locker_app/app.py"

guake --split-vertical
guake -e "$anaconda_env_activate  && clear" 
guake -e "python locker_service/locker_service.py"

guake --split-horizontal -e "$anaconda_env_activate  && clear"
guake -e "python locker_service/rabbitmq_receive_from_user_service.py"

#create mongo tab
guake --new-tab $locker_app_path -r "Mongo"
guake -e "$anaconda_env_activate && cd locker_service/mongo_db  && clear"
guake -e "mongod --port 27017 --dbpath ./db0 --replSet lockers_rs"

guake --split-vertical -e "$anaconda_env_activate  && clear"
guake -e "mongod --port 27018 --dbpath ./db1 --replSet lockers_rs"

guake --split-horizontal -e "$anaconda_env_activate  && clear"
guake -e "mongod --port 27019 --dbpath ./db2 --replSet lockers_rs"

# create hazelcast and rabbitmq
guake --new-tab $locker_app_path -r "HazelRabbit"
# guake -e "hazel"

guake --split-vertical 
guake -e "$anaconda_env_activate  && clear"
guake -e "rabbitmq-server"

# create git
guake --new-tab $locker_app_path -r "GitLockerApp"