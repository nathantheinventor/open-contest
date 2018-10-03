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
    apt-get -y install nodejs npm python3 docker.io psmisc && \
    npm install -g nodemon

# COPY . /code
# COPY web/ /web/
# COPY serve/ /serve
# COPY generator/ /generator/
# COPY setup.js /setup.js

ENTRYPOINT ["nodemon", "-w", "/code", "/code/setup.js"]
