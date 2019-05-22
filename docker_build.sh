#!/bin/bash

PROJECT_NAME=$1

docker build \
       --tag=notebook_$PROJECT_NAME \
       -f ./Dockerfile \
       --build-arg user=`id -u` \
       --build-arg group=`id -g` \
       --build-arg project=$PROJECT_NAME \
       .
