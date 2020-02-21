#!/bin/bash

# Get directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

IPADDR=0.0.0.0
PORT=80
DBDIR=$DIR/../db
LOG_LEVEL=INFO

LOGTOFILE="--logto /db/opencontest.log"
DISABLE_REQ_LOG="--log-5xx --log-4xx --disable-logging"

while [ $# -ne 0 ]; do
  if [ $1 == -p ]; then
    PORT=$2
    shift
  elif [ $1 == --log-all-requests ]; then
    unset DISABLE_REQ_LOG
  elif [ $1 == -db ]; then
    DBDIR=$2
    shift
  elif [ $1 == --log-debug ]; then
    LOG_LEVEL='DEBUG'
  elif [ $1 == --local-only ]; then
    IPADDR=127.0.0.1
  elif [ $1 == --log-stdout ]; then
    unset LOGTOFILE
  else
    echo "Usage: dev.sh [-p port#] [-db path] [--log-all-requests] [--log-stdout] [--local-only]"
    exit 1
  fi

  shift
done


DBDIR=$(realpath $DBDIR)

echo "Using database directory: $DBDIR"

if [ ! -e $DBDIR ]; then 
  mkdir $DBDIR
fi

export USER="bjucps"
export OC_PROJECT_NAME="open-contest"
export OC_CODE_DIR=$DIR/opencontest

cd $OC_CODE_DIR
if [ ! -z "$LOGTOFILE" ]; then
  echo Logging to $DBDIR/opencontest.log.
fi

# Get group id of docker group
GID=$(getent group docker | cut -d: -f3)

RUNCMD="docker run \
    --rm \
    --user=$UID:$GID \
    -v $DBDIR:/db \
    -v $OC_CODE_DIR/:/code \
    -v /tmp:/tmp \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -p $IPADDR:$PORT:8000/tcp \
    -e OC_LOG_LEVEL=$LOG_LEVEL \
    $USER/$OC_PROJECT_NAME \
    $LOGTOFILE \
    $DISABLE_REQ_LOG" 

echo Starting open-contest server at port $PORT.
echo $RUNCMD
$RUNCMD

