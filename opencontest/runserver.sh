#!/bin/bash

/usr/sbin/nginx
uwsgi --threads 10 --socket 0.0.0.0:8001 --module opencontest.wsgi
