#!/bin/sh

#chmod +x locker_app_tab.sh
locker_app_path="$HOME/Uni/2nd_semester/Distributed/LockerApp"
# change env_name to your env name
anaconda_env_activate="conda activate p36_cvm_project"

# create locker tab
guake --new-tab $locker_app_path -r "LockerAppUserService"
guake -e "$anaconda_env_activate && clear"
guake -e "python locker_app/app.py"

guake --split-vertical
guake -e "$anaconda_env_activate && clear"
guake -e "python user_service/user_service.py"

#create postgres tab
guake --new-tab $locker_app_path -r "PostgresHazelRabbit"
guake -e "$anaconda_env_activate && clear"
guake -e "sudo service postgresql start"

guake --split-vertical -e "$anaconda_env_activate && clear"
#guake -e "hazel"

guake --split-horizontal -e "$anaconda_env_activate && clear"
guake -e "rabbitmq-server"

# create git
guake --new-tab $locker_app_path -r "GitLockerApp"