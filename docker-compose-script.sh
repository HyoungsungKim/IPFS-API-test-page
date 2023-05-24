#!/bin/bash

docker-compose down

sudo chmod -R 777 ./Private-IPFS/*
sudo chmod -R 777 ./rqlite-db/*
docker-compose build
docker-compose up