#!/bin/sh
workdir=$(pwd)
docker run -it --name 'admin-dev' -v $workdir:/admin fury1/admin-dev bash