ARG USER=heast
# ARG OC_PROJECT_NAME=open-contest-django
ARG OC_PROJECT_NAME=oc-test
ARG PROJECT_PATH=~/open-contest/opencontest

# Include all the mini-dockerfiles used for contest submissions in this build.
FROM $USER/$OC_PROJECT_NAME-c-runner
FROM $USER/$OC_PROJECT_NAME-cpp-runner
FROM $USER/$OC_PROJECT_NAME-cs-runner
FROM $USER/$OC_PROJECT_NAME-java-runner
FROM $USER/$OC_PROJECT_NAME-python3-runner
FROM $USER/$OC_PROJECT_NAME-ruby-runner
FROM $USER/$OC_PROJECT_NAME-vb-runner

FROM ubuntu:bionic

# Install dependencies.
COPY setup.sh /setup.sh
RUN ./setup.sh

ADD requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# Symlink the nginx config so that nginx can find it.
RUN ln -s $PROJECT_PATH/nginx.conf /etc/nginx/sites-enabled/
# RUN ln -s -f /usr/bin/python3 /usr/bin/python

COPY . $PROJECT_PATH/
COPY uwsgi_params /uwsgi_params
COPY runserver.sh /runserver.sh

ENTRYPOINT ["uwsgi", "--threads", "10", "--http", "0.0.0.0:8000", "--module", "opencontest.wsgi"]

# Note: use the following build and run commands:
# sudo docker build --rm=true --force-rm=true -t [name:tag] .
# sudo docker run -v /tmp:/tmp -v /path/to/db:/db -v /var/run/docker.sock:/var/run/docker.sock -p :8000:8000 [name]
