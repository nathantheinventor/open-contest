const {Storage} = require("@google-cloud/storage");
const {readFile, mkdir} = require("fs");
const {join} = require("path");
const {exec} = require("child_process");
const extract = require("extract-zip");

let project = "project";
let db = "db";

exports.run = async (event, callback) => {
    console.log("New Run ---------------------------------------")
    project = process.env.GCLOUD_PROJECT;
    console.log(event);
    db = `${project}-db`;
    const filename = event.name;
    const bucket = event.bucket;
    await downloadFile(bucket, filename, "submission.json");
    const settings = await readJSONFile("/tmp/submission.json");
    await downloadFile(db, `submissions/${settings.submission}/code.cpp`, "code.cpp");
    await execProgram(`g++ -std=c++11 -O2 /tmp/code.cpp -o /tmp/code > /tmp/out.txt 2> /tmp/err.txt`);
    uploadFile(db, `submissions/${settings.submission}/results/out.txt`, `out.txt`);
    uploadFile(db, `submissions/${settings.submission}/results/err.txt`, `err.txt`);
    for (var i = 0; i < settings.tests; i ++) {
        await downloadFile(db, `problems/${settings.problem}/testData/in${i}.txt`, `in${i}.txt`);
    }
    for (var i = 0; i < settings.tests; i ++) {
        await execProgram(`unshare -n /tmp/code < /tmp/in${i}.txt > /tmp/out${i}.txt 2> /tmp/err${i}.txt`);
    }
    for (var i = 0; i < settings.tests; i ++) {
        uploadFile(db, `submissions/${settings.submission}/results/out${i}.txt`, `out${i}.txt`);
        uploadFile(db, `submissions/${settings.submission}/results/err${i}.txt`, `err${i}.txt`);
    }
    callback();
}


async function downloadFile(bucket, filename, outputFile) {
    const storage = new Storage();
    return storage
            .bucket(bucket)
            .file(filename)
            .download({destination: join("/tmp", outputFile)});
}

async function uploadFile(bucket, filename, localFile) {
    const storage = new Storage();
    return storage
            .bucket(bucket)
            .upload(join("/tmp", localFile), {
                destination: filename
            });
}



// async function mkDir(dir) {
//     return new Promise((resolve, reject) => {
//         mkdir(dir, err => {
//             if (err) reject(err);
//             else resolve();
//         });
//     });
// }

// async function extractZip(zip, dir) {
//     return new Promise((resolve, reject) => {
//         extract(zip, {dir: dir}, err => {
//             if (err) reject(err);
//             else resolve();
//         });
//     });
// }

async function readJSONFile(file) {
    return new Promise((resolve, reject) => {
        readFile(file, (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(JSON.parse(data.toString()));
            }
        });
    });
}

async function execProgram(command) {
    return new Promise((resolve, reject) => {
        exec(command, (err, stdout, stderr) => {
            console.log(stdout);
            console.error(stderr);
            console.error(err);
            // if (err) {
            //     reject(err);
            // } else {
                resolve();
            // }
        });
    });
}
