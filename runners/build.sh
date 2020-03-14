#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function build_image {
    DIRECTORY=$1
    IMAGE=$2

    echo Building $2...
    docker build $DIRECTORY -t $OC_DOCKERIMAGE_BASE-$IMAGE

}

cd $DIR

source ../open-contest.config

# Build Docker images
build_image c/       c-runner
build_image cpp/     cpp-runner
build_image cs/      cs-runner
build_image java/    java-runner
build_image python3/ python3-runner
build_image ruby/    ruby-runner
build_image vb/      vb-runner

# Push Docker images to DockerHub
if [ "$1" == "push" ]
then
docker push $OC_DOCKERIMAGE_BASE-c-runner
docker push $OC_DOCKERIMAGE_BASE-cpp-runner
docker push $OC_DOCKERIMAGE_BASE-cs-runner
docker push $OC_DOCKERIMAGE_BASE-java-runner
docker push $OC_DOCKERIMAGE_BASE-python3-runner
docker push $OC_DOCKERIMAGE_BASE-ruby-runner
docker push $OC_DOCKERIMAGE_BASE-vb-runner
fi
