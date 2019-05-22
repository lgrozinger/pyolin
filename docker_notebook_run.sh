#!/bin/bash

PROJECT_NAME=$1
PROJECT_PATH=$2

docker run -it --rm \
       -v $PROJECT_PATH:/$PROJECT_NAME \
       -p 8888:8888 \
       notebook_$PROJECT_NAME
