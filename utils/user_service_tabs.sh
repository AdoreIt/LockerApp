#!/bin/sh

# chmod +x user_service_tabs.sh

# change ... to your path
locker_app_path="$HOME/Uni/2nd_semester/Distributed/LockerApp"
# change env_name to your env name
anaconda_env_activate="conda activate p36_cvm_project"

# create locker tab
guake --new-tab $locker_app_path -r "LockerAppUserService"
guake -e "$anaconda_env_activate && clear"

guake --split-vertical
guake -e "$anaconda_env_activate && clear"

#create postgres tab
guake --new-tab $locker_app_path -r "PostgresHazelRabbit" 
guake -e "$anaconda_env_activate && clear" 

guake --split-vertical -e "$anaconda_env_activate && clear"
guake --split-horizontal -e "$anaconda_env_activate && clear"

# create git
guake --new-tab $locker_app_path -r "GitLockerApp"
