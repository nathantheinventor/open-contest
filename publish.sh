#! /bin/bash
if [ hash npm ]; then
    echo ""
else
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
npm i typescript
tsc
cd bin/web/
gcloud functions deploy index --entry-point=test --project=$PROJECT --trigger-http
