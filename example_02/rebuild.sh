#!/bin/bash

# Config
IMAGE="alpine-python-falcon-examples-02"
STARTARGS="-p 80:80"

# Colors
CDE="\033[39m"
CYE="\033[33m"
CBL="\033[34m"

echo -e "${CYE}Trying to remove CONTAINER tagged: ${CBL}${IMAGE}${CDE}"
docker rm $IMAGE

echo -e "${CYE}Trying to remove IMAGE: ${CBL}${IMAGE}${CDE}"
docker rmi $IMAGE

echo -e "${CYE}Trying to build IMAGE, tagging: ${CBL}${IMAGE}${CDE}"
time docker build -t $IMAGE .

echo -e "${CYE}Trying to start CONTAINER tagged: ${CBL}${IMAGE}${CDE}"
docker run --name $IMAGE $STARTARGS $IMAGE

