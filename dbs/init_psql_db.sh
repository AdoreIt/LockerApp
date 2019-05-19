#!/usr/bin/env bash

sudo -u postgres psql -f ./migrations_psql/create_dbs.sql -U postgres
sudo -u postgres psql -f ./migrations_psql/migrations_lockers.sql -U postgres -d users_db
