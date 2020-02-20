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

export USER="bjucps"
export OC_PROJECT_NAME="open-contest"
export OC_CODE_DIR=$DIR/opencontest

cd $OC_CODE_DIR
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $DBDIR:/db \
    -v /tmp:/tmp \
    -v $OC_CODE_DIR/:/code \
    -p 0.0.0.0:8000:8000/tcp \
    $USER/$OC_PROJECT_NAME \
    --ini uwsgi.ini
