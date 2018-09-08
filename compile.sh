#! /bin/bash
if [ which npm ]; then
    echo ""
else
    apt-get install -y curl
    curl -sL https://deb.nodesource.com/setup_10.x | bash
    apt-get install -y nodejs
fi
if [ which tsc ]; then
    echo ""
else
    npm i typescript -g
fi
tsc
