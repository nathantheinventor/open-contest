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
if [ hash gcloud ]; then
    echo ""
else
    # Create environment variable for correct distribution
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
    # Add the Cloud SDK distribution URI as a package source
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    # Import the Google Cloud Platform public key
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    # Update the package list and install the Cloud SDK
    apt-get update && apt-get install -y google-cloud-sdk
fi
tsc
cd bin/web/
gcloud functions deploy index --entry-point=test --project=$PROJECT --trigger-http
