#!/bin/bash

docker build -t yuanlii/custom_psql .

docker network create -d bridge my-bridge-network

docker run -t --rm -d -p 5432:5432 --network my-bridge-network --name custom_psql_running yuanlii/custom_psql
