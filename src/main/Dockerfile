ARG USER=nathantheinventor
ARG OC_PROJECT_NAME=open-contest-dev

FROM $USER/$OC_PROJECT_NAME-c-runner
FROM $USER/$OC_PROJECT_NAME-cpp-runner
FROM $USER/$OC_PROJECT_NAME-cs-runner
FROM $USER/$OC_PROJECT_NAME-java-runner
FROM $USER/$OC_PROJECT_NAME-python2-runner
FROM $USER/$OC_PROJECT_NAME-python3-runner
FROM $USER/$OC_PROJECT_NAME-ruby-runner
FROM $USER/$OC_PROJECT_NAME-vb-runner

FROM ubuntu:bionic

RUN apt-get update && \
    apt-get -y install nodejs npm python3 python3-pip docker.io psmisc nginx
RUN npm install -g nodemon
RUN pip3 install markdown2 uwsgi readerwriterlock
RUN ln -s -f /usr/bin/python3 /usr/bin/python

COPY . /code
COPY runserver.sh /runserver.sh
COPY uwsgi_params /uwsgi_params
# COPY web/ /web/
# COPY serve/ /serve
# COPY generator/ /generator/
# COPY setup.js /setup.js

# ENTRYPOINT ["nodemon", "-w", "/code", "-e", "js,py", "--exec", "uwsgi --http :8000 --module", "code"]
ENTRYPOINT [ "uwsgi", "--threads", "10", "--http", "0.0.0.0:8000", "--static-map", "/static=/code/serve", "--module", "code", "--log-5xx", "--disable-logging" ]
# ENTRYPOINT [ "bash", "/runserver.sh" ]
