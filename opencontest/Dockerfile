ARG USER=bjucps
ARG OC_PROJECT_NAME=open-contest
ARG PROJECT_PATH=~/open-contest/opencontest

# Include all the mini-dockerfiles used for contest submissions in this build.
#FROM $USER/$OC_PROJECT_NAME-c-runner
#FROM $USER/$OC_PROJECT_NAME-cpp-runner
#FROM $USER/$OC_PROJECT_NAME-cs-runner
#FROM $USER/$OC_PROJECT_NAME-java-runner
FROM $USER/$OC_PROJECT_NAME-python3-runner
#FROM $USER/$OC_PROJECT_NAME-ruby-runner
#FROM $USER/$OC_PROJECT_NAME-vb-runner

FROM bjucps/open-contest-base


# Symlink the nginx config so that nginx can find it.
#RUN ln -s $PROJECT_PATH/nginx.conf /etc/nginx/sites-enabled/
# RUN ln -s -f /usr/bin/python3 /usr/bin/python

RUN mkdir /code
COPY . /code

EXPOSE 8000
WORKDIR /code
ENTRYPOINT ["uwsgi", "--threads", "10", "--http", "0.0.0.0:8000", "--module", "opencontest.wsgi"]

# Note: use the following build and run commands:
# sudo docker build --rm=true --force-rm=true -t bjucps/open-contest .
# sudo docker run -v /tmp:/tmp -v $HOME/db:/db -v /var/run/docker.sock:/var/run/docker.sock -p 80:8000 bjucps/open-contest

# To run, overriding open-contest code in the image with code in current directory:
# sudo docker run -v $(pwd):/code -v /tmp:/tmp -v $HOME/db:/db -v /var/run/docker.sock:/var/run/docker.sock -p 80:8000 bjucps/open-contest


# If setup.sh or requirements.txt changes, execute the following build command, then rebuild open-contest using the above command:
# sudo docker build --rm=true --force-rm=true -f Dockerfile-base -t bjucps/open-contest-base .
