#!/bin/bash

cp .env.example .env

sed -i "s/DJANGO__SECRET_KEY=.*/DJANGO__SECRET_KEY='$(openssl rand -hex 64)'/g" .env
sed -i "s|POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD='$(openssl rand -base64 64 | tr -d '\n' | tr -d '~' | tr -d "'")'|g" .env
sed -i "s/RABBITMQ_PASSWORD=.*/RABBITMQ_PASSWORD='$(openssl rand -hex 32)'/g" .env
sed -i "s/PGADMIN_DEFAULT_PASSWORD=.*/PGADMIN_DEFAULT_PASSWORD='$(openssl rand -hex 32)'/g" .env
sed -i "s/DJANGO_SUPERUSER_PASSWORD=.*/DJANGO_SUPERUSER_PASSWORD='$(openssl rand -hex 16)'/g" .env

cp docker-compose.override.dev.yml docker-compose.override.yml