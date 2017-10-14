#!/bin/bash

HOST="51.15.195.60"
PROJECT_PATH="/root/papyrus"

rsync -azP . root@$HOST:$PROJECT_PATH
ssh root@$HOST "export DOCKER_COMPOSE_ENV=pro && cd $PROJECT_PATH && docker-compose down && docker-compose up -d"
