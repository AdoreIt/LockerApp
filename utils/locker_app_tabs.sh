#!/bin/sh

#chmod +x locker_app_tabs.sh

# change ... to your path
locker_app_path="$HOME/.../LockerApp"
# change env_name to your env name
anaconda_env_activate="conda activate env_name"

# create locker tab
guake --new-tab $locker_app_path -r "LockerAppUserServiceRecieve"
guake -e "$anaconda_env_activate && clear"

guake --split-vertical
guake -e "$anaconda_env_activate && clear"
guake --split-horizontal -e "$anaconda_env_activate && clear"

#create mongo tab
guake --new-tab "$locker_app_path/locker_service/mongo_db" -r "Mongo" 
guake -e "$anaconda_env_activate && clear" 
guake --split-vertical -e "$anaconda_env_activate && clear"
guake --split-horizontal -e "$anaconda_env_activate && clear"

# create hazelcast and rabbitmq
guake --new-tab $locker_app_path -r "HazelRabbit" -e "clear"
guake --split-vertical -e "$anaconda_env_activate && clear"

# create git
guake --new-tab $locker_app_path -r "GitLockerApp"
