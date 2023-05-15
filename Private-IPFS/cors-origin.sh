#!/bin/bash

ALLOW_ORIGINS='"http://0.0.0.0:3000/", "http://localhost:5001", "https://webui.ipfs.io", "https://dev.webui.ipfs.io", "http://172.20.0.3:3000", "*"'
#ALLOW_ORIGINS='"*"'

# stop executing if anything fails
set -e

ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin "[$ALLOW_ORIGINS]"
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods '["PUT", "POST", "GET"]'


echo "IPFS API CORS headers configured for $ALLOW_ORIGINS"
echo "Please restart your IPFS daemon"