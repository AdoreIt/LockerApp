#!/usr/bin/env bash

sudo -u postgres psql -f ./migrations_psql/drop_users_db.sql -U postgres
