#! /bin/bash
if [ hash npm ]; then
    echo ""
else
    apt-get -y install node
fi
npm i typescript
tsc
cd bin/web/
gcloud functions deploy index --entry-point=test --project=$PROJECT --trigger-http
