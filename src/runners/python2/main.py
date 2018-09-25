import os
import sys
from google.cloud import storage
from datetime import datetime
import json

def download(bucket: str, bucketFilename: str, localFilename: str):
    storage                   \
        .Client()             \
        .get_bucket(bucket)   \
        .blob(bucketFilename) \
        .download_to_filename(localFilename)

def upload(bucket: str, bucketFilename: str, localFilename: str):
    storage                   \
        .Client()             \
        .get_bucket(bucket)   \
        .blob(bucketFilename) \
        .upload_from_filename(localFilename)

def readJSONFile(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.loads(f.read())

def run(data, context):
    print(data)
    print(context)
    db = os.environ["GCLOUD_PROJECT"] + "-db"
    download(data["bucket"], data["name"], "/tmp/submission.json")
    settings = readJSONFile("/tmp/submission.json")
    download(db, "submissions/{}/code.cpp".format(settings["submission"]), "/tmp/code.cpp")
    os.system("g++ -std=c++11 -O2 /tmp/code.cpp -o /tmp/code > /tmp/out.txt 2> /tmp/err.txt")
    with open("/tmp/out.txt", "r") as f:
        print(f.read())
    with open("/tmp/err.txt", "r") as f:
        print(f.read(), file=sys.stderr)
    totalTime = datetime.now() - datetime.now()
    for i in range(int(settings["tests"])):
        download(db, "problems/{}/testData/in{}.txt".format(settings["problem"], i), "/tmp/in.txt")
        a = datetime.now()
        os.system("unshare -n /tmp/code < /tmp/in.txt > /tmp/out.txt 2> /tmp/err.txt")
        b = datetime.now()
        totalTime += b - a
        upload(db, "submissions/{}/results/out{}.txt".format(settings["submission"], i), "/tmp/out.txt")
        upload(db, "submissions/{}/results/err{}.txt".format(settings["submission"], i), "/tmp/err.txt")
    print(totalTime)
