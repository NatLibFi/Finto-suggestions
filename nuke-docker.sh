#!/bin/sh
# This scripts nukes docker totally, removes all container, images, volumes
# After that runs docker-compose up everything
yes | docker system prune -a && yes | docker volume prune && docker-compose up --build