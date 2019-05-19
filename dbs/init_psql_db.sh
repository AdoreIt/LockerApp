#!/usr/bin/env bash

sudo -u postgres psql -f ./migrations_psql/create_users_db.sql -U postgres
sudo -u postgres psql -f ./migrations_psql/create_users_table.sql -U postgres -d users_db
