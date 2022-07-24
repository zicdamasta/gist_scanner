#!/usr/bin/env bash

echo "Running checks..."
if [ -z "$1" ]; then
  echo "Missing VERSION_TAG"
  exit 2
fi


VERSION_TAG=$1

cd /home/ubuntu/docker/gist-scanner

function update_env {
  ENV_PATH=$1
  echo "Updating version tag to $VERSION_TAG in $ENV_PATH"
  perl -i -pe "s/(?<=VERSION_TAG=).*/$VERSION_TAG/" $ENV_PATH

}

update_env .env
sudo docker-compose down
sudo docker-compose up -d