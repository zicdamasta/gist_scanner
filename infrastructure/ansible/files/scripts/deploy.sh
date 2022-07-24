#!/usr/bin/env bash

echo "Running checks..."
if [ -z "$1" ]; then
  echo "Missing VERSION_TAG"
  exit 2
fi
if [ -z "$2" ]; then
  echo "Missing DOCKER_USERNAME"
  exit 2
fi
if [ -z "$3" ]; then
  echo "Missing DOCKER_PASSWORD"
  exit 2
fi



VERSION_TAG=$1
DOCKER_USERNAME=$2
DOCKER_PASSWORD=$3

cd /home/ubuntu/docker/gist-scanner

function update_env {
  ENV_PATH=$1
  echo "Updating version tag to $VERSION_TAG in $ENV_PATH"
  perl -i -pe "s/(?<=VERSION_TAG=).*/$VERSION_TAG/" $ENV_PATH

}

# docker login
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
update_env .env
sudo docker-compose down
sudo docker-compose up -d