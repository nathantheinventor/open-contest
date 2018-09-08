#! /bin/bash
if [ hash npm ]; then
    echo ""
else
    curl -sL https://deb.nodesource.com/setup_10.x | bash
    apt-get install -y nodejs
fi
if [ hash tsc ]; then
    echo ""
else
    npm i typescript -g
fi
tsc
