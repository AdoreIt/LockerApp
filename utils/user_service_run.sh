#!/bin/sh

# chmod +x user_service_run.sh

# change ... to your path
locker_app_path="$HOME/.../LockerApp"
# change env_name to your env name
anaconda_env_activate="conda activate p36_lockerapp"

# create locker tab
guake --new-tab $locker_app_path -r "LockerAppUserService"
guake -e "$anaconda_env_activate && clear"
guake -e "python locker_app/app.py"

guake --split-vertical
guake -e "$anaconda_env_activate && clear"
guake -e "python user_service/user_service.py"

#create postgres, haproxy, hazelcast, rabbitmq  tab
guake --new-tab $locker_app_path -r "PostgresHAproxyHazelRabbit"
guake -e "$anaconda_env_activate && clear"
guake -e "service postgresql start && haproxy -f config/haproxy.cfg"

guake --split-vertical -e "$anaconda_env_activate && clear"
guake -e "./locker_app/hazelcast_locker_app/bin/stop.sh; ./locker_app/hazelcast_locker_app/bin/start.sh"

guake --split-horizontal -e "$anaconda_env_activate && clear"
guake -e "rabbitmq-server"

# create git
guake --new-tab $locker_app_path -r "GitLockerApp"
