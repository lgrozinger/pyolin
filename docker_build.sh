#!/bin/bash

docker build \
       --tag=notebook_pyolin \
       -f ./Dockerfile \
       .
