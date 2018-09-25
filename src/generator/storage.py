import os
from google.cloud import storage
import json

db = os.environ["GCLOUD_PROJECT"] + "-db"

def getDBFile(filename: str) -> dict:
    return json.loads(
        storage                   \
            .Client()             \
            .get_bucket(db)       \
            .blob(filename)       \
            .download_as_string()
    )

webBucket = os.environ["WEB_BUCKET"]
def uploadHTMLFile(filename: str):
    storage                    \
        .Client()              \
        .get_bucket(webBucket) \
        .blob(filename)        \
        .upload_from_filename("/tmp/serve/" + filename)

def listProblems() -> list:
    blob = storage.Client().get_bucket(db).list_blobs(delimiter="/", prefix="problems/")
    problems = []
    for i in blob:
        if i.name != "problems/":
            problems.append(i.name.split("/")[1].split(".")[0])
    return problems

def listContests() -> list:
    blob = storage.Client().get_bucket(db).list_blobs(delimiter="/", prefix="contests/")
    problems = []
    for i in blob:
        if i.name != "contests/":
            problems.append(i.name.split("/")[1].split(".")[0])
    return problems

