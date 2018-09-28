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
    apt-get -y install nodejs python3 docker.io

COPY web/ /web/
COPY static/ /serve/static
COPY generator/ /generator/
COPY setup.js /setup.js

ENTRYPOINT ["node", "/setup.js"]
