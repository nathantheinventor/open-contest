export USER="nathantheinventor"
export OC_PROJECT_NAME="open-contest-dev-2"
docker run -v /var/run/docker.sock:/var/run/docker.sock -v /tmp/db:/db -v /tmp:/tmp -v /Users/nathancollins/code/open-contest/src/main/:/code -p 0.0.0.0:8002:8000/tcp $USER/$OC_PROJECT_NAME
