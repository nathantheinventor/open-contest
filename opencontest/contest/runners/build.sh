#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $DIR/../../../open-contest.config
source ~/.open-contest

# Build Docker images
docker build c/       -t $OC_DOCKERIMAGE_BASE-c-runner
docker build cpp/     -t $OC_DOCKERIMAGE_BASE-cpp-runner
docker build cs/      -t $OC_DOCKERIMAGE_BASE-cs-runner
docker build java/    -t $OC_DOCKERIMAGE_BASE-java-runner
docker build python3/ -t $OC_DOCKERIMAGE_BASE-python3-runner
docker build ruby/    -t $OC_DOCKERIMAGE_BASE-ruby-runner
docker build vb/      -t $OC_DOCKERIMAGE_BASE-vb-runner

# Push Docker images to DockerHub
#docker push $OC_DOCKERIMAGE_BASE-c-runner
#docker push $OC_DOCKERIMAGE_BASE-cpp-runner
#docker push $OC_DOCKERIMAGE_BASE-cs-runner
#docker push $OC_DOCKERIMAGE_BASE-java-runner
#docker push $OC_DOCKERIMAGE_BASE-python3-runner
#docker push $OC_DOCKERIMAGE_BASE-ruby-runner
#docker push $OC_DOCKERIMAGE_BASE-vb-runner
