#!/bin/bash

# Get directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ $# -eq 1 ]; then
  DBDIR=$1
else
  DBDIR=$DIR/../db
fi

DBDIR=$(realpath $DBDIR)

echo "Using database directory: $DBDIR"

if [ ! -e $DBDIR ]; then 
  mkdir $DBDIR
fi

export USER="nathantheinventor"
export OC_PROJECT_NAME="open-contest"
export OC_CODE_DIR=$DIR/src/main
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $DBDIR:/db \
    -v /tmp:/tmp \
    -v $OC_CODE_DIR/:/code \
    -v $OC_CODE_DIR/nginx.conf:/etc/nginx/sites-enabled/nginx.conf \
    -p 0.0.0.0:8000:8000/tcp \
    $USER/$OC_PROJECT_NAME
