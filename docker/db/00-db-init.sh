#!/usr/bin/env bash

set -o verbose

# Change template1
gosu postgres psql postgres -c \
  "UPDATE pg_database SET datistemplate=FALSE WHERE datname='template1';"
gosu postgres psql postgres -c \
  "DROP DATABASE template1;"
gosu postgres psql postgres -c \
  "CREATE DATABASE template1 WITH owner=postgres template=template0 encoding='UTF8' lc_collate='en_US.utf8';"
gosu postgres psql postgres -c \
  "UPDATE pg_database SET datistemplate=TRUE WHERE datname='template1';"

# Create extensions on template1
gosu postgres psql template1 -c 'CREATE EXTENSION IF NOT EXISTS hstore;'
gosu postgres psql template1 -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'

# Create database
gosu postgres psql -c "DROP DATABASE IF EXISTS ${POSTGRES_DB};"

gosu postgres createuser "${POSTGRES_USER}"

gosu postgres createdb --owner "${POSTGRES_USER}" --template template1 \
    --encoding=UTF8 --lc-ctype=en_US.utf8 --lc-collate=en_US.utf8 "${POSTGRES_DB}";
