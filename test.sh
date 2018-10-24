export USER="nathantheinventor"
export OC_PROJECT_NAME="open-contest-dev"
docker run -v /var/run/docker.sock:/var/run/docker.sock -v /tmp/db:/db -v /tmp:/tmp -v /Users/nathancollins/code/open-contest/src/main/:/code -p 127.0.0.1:8000:8000/tcp $USER/$OC_PROJECT_NAME "Nathan Collins" 8000