#!/bin/bash

docker-compose -f docker-compose.dev.yml exec web ./manage.py makemigrations
docker-compose -f docker-compose.dev.yml exec web ./manage.py migrate