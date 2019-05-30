#!/bin/bash

docker run -it --rm \
       -v $1:/pyolin/data \
       -v $2:/pyolin/ucf \
       -p 8888:8888 \
       notebook_pyolin
