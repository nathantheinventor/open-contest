export USER="nathantheinventor"
export OC_PROJECT_NAME="open-contest"
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ~/db:/db \
    -v /tmp:/tmp \
    -v /Users/nathancollins/code/open-contest/src/main/:/code \
    -v /Users/nathancollins/code/open-contest/src/main/nginx.conf:/etc/nginx/sites-enabled/nginx.conf \
    -p 0.0.0.0:8000:8000/tcp \
    $USER/$OC_PROJECT_NAME
