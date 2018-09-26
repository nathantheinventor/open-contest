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

# RUN apt-get update && \
#     apt-get -y install apt-transport-https ca-certificates curl software-properties-common && \
#     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
#     add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" && \
#     apt-get update && \
#     apt-get -y install nodejs python3 docker-ce

RUN apt-get update && \
    apt-get -y install nodejs python3 docker.io

COPY web/ /web/
COPY static/ /serve/static
COPY generator/ /generator/
COPY test/ /test/
COPY run.sh /run.sh

ENTRYPOINT ["bash", "/run.sh"]
