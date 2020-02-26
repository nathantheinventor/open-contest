#!/bin/bash

# Get directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

OC_DOCKERIMAGE_BASE=bjucps/open-contest
OC_MAX_OUTPUT_LEN=10000  # (bytes) Submission output larger than this is discarded
OC_MAX_DISPLAY_LEN=500    # (bytes) Submission output larger than this is not displayed
OC_MAX_DISPLAY_LINES=30    # (lines) Submission output having more lines than this is not displayed

OC_CODE_DIR=$DIR/opencontest

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
  elif [ $1 == -dev ]; then
    OC_CODE_OPT="-v $OC_CODE_DIR/:/code"
  elif [ $1 == --log-debug ]; then
    LOG_LEVEL='DEBUG'
  elif [ $1 == --local-only ]; then
    IPADDR=127.0.0.1
  elif [ $1 == --log-stdout ]; then
    unset LOGTOFILE
  else
    echo "Usage: dev.sh [-dev] [-p port#] [-db path] [--log-all-requests] [--log-stdout] [--local-only]"
    exit 1
  fi

  shift
done


DBDIR=$(realpath $DBDIR)

echo "Using database directory: $DBDIR"

if [ ! -e $DBDIR ]; then 
  mkdir $DBDIR
fi

LOGFILE=$DBDIR/opencontest.log
if [ ! -z "$LOGTOFILE" ]; then
  echo Logging to $LOGFILE.
  if [ -e $LOGFILE ]; then
    mv $LOGFILE $LOGFILE.old
  fi
fi

# Get group id of docker group
GID=$(getent group docker | cut -d: -f3)

RUNCMD="docker run \
    --rm \
    --user=$UID:$GID \
    -v $DBDIR:/db \
    $OC_CODE_OPT
    -v /tmp:/tmp \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -p $IPADDR:$PORT:8000/tcp \
    -e OC_LOG_LEVEL=$LOG_LEVEL \
    -e OC_MAX_OUTPUT_LEN=$OC_MAX_OUTPUT_LEN \
    -e OC_MAX_DISPLAY_LEN=$OC_MAX_DISPLAY_LEN \
    -e OC_MAX_DISPLAY_LINES=$OC_MAX_DISPLAY_LINES \
    -e OC_DOCKERIMAGE_BASE=$OC_DOCKERIMAGE_BASE \
    $OC_DOCKERIMAGE_BASE \
    $LOGTOFILE \
    $DISABLE_REQ_LOG" 

echo Starting open-contest server at port $PORT.
echo $RUNCMD
$RUNCMD

