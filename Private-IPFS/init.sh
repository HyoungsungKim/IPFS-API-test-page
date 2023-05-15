#!/bin/bash

apt-get update

set -e

if [ ! -d "config" ]; then
  echo "Already exist config"  
  #chmod 777 cors-origin.sh
  #./cors-origin.sh
  ipfs daemon --init-config=config
else
  echo "Initialize ipfs"
  ipfs init config
  chmod 777 cors-origin.sh
  ./cors-origin.sh
  ipfs daemon --init-config=config
fi


