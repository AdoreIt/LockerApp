#!/usr/bin/env bash

sudo -u postgres psql -f ./migrations_psql/drop_dbs.sql -U postgres
