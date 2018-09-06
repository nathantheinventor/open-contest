#! /bin/bash
npm i typescript
tsc
cd bin/web/
gcloud functions deploy index --entry-point=test --project=$PROJECT --trigger-http
