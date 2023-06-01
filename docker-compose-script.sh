#!/bin/bash

docker-compose down

sudo chmod -R 777 ./Private-IPFS/*
docker-compose build
docker-compose up