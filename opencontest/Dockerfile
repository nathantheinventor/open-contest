ARG USER=bjucps
ARG OC_PROJECT_NAME=open-contest

# Include all the mini-dockerfiles used for contest submissions in this build.
FROM $USER/$OC_PROJECT_NAME-c-runner
FROM $USER/$OC_PROJECT_NAME-cpp-runner
FROM $USER/$OC_PROJECT_NAME-cs-runner
FROM $USER/$OC_PROJECT_NAME-java-runner
FROM $USER/$OC_PROJECT_NAME-python3-runner
FROM $USER/$OC_PROJECT_NAME-ruby-runner
FROM $USER/$OC_PROJECT_NAME-vb-runner

FROM python:3.8-buster
RUN apt-get update 

# Install dependencies.
RUN apt-get install -y docker.io psmisc 
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# Copy code
RUN mkdir /code
COPY . /code

EXPOSE 8000
WORKDIR /code
ENTRYPOINT ["uwsgi", "--threads", "50", "--http", "0.0.0.0:8000", "--module", "opencontest.wsgi", "--ini", "uwsgi.ini"]

# Note: use the following build and run commands:
# docker build --rm --force-rm -t bjucps/open-contest .
# To publish it to dockerhub:
# docker push bjucps/open-contest-base

# To run :
# docker run -v /tmp:/tmp -v $HOME/db:/db -v /var/run/docker.sock:/var/run/docker.sock -p 80:8000 bjucps/open-contest

# To run, overriding open-contest code in the image with code in current directory:
# docker run -v $(pwd):/code -v /tmp:/tmp -v $HOME/db:/db -v /var/run/docker.sock:/var/run/docker.sock -p 80:8000 bjucps/open-contest
