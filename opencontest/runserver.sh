#!/bin/bash

#/usr/sbin/nginx
#uwsgi --threads 10 --socket 0.0.0.0:8000 --module opencontest.wsgi

# Comment out the line below to have logging go to stdout
LOGOPT="--logto /db/opencontest.log"

echo Starting open-contest server. Logging to $HOME/db/opencontest.log.
docker run -v $(pwd):/code -v /tmp:/tmp -v $HOME/db:/db -v /var/run/docker.sock:/var/run/docker.sock -p 80:8000 bjucps/open-contest --ini uwsgi.ini $LOGOPT
