#!/bin/sh

#chmod +x guake_create_tab.sh
locker_app_path="$HOME/AdoreIt/LockerApp"

guake --new-tab $locker_app_path -r "LockerApp" -e "cd locker_app"
guake --split-vertical -e "cd ../locker_service"
guake --split-horizontal