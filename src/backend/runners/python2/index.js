const {Storage} = require("@google-cloud/storage");
const {readFile} = require("fs");

exports.run = (event, callback) => {
    console.log(event);
    const storage = new Storage({projectId: process.env._PROJECT});
    const filename = event.data.name;
    storage
        .bucket(event.data.bucket)
        .file(filename)
        .download({
            destination: `/tmp/${filename}`
        })
        .then(_ => {
            readFile(`/tmp/${filename}`, (err, data) => {
                console.log(data.toString());
                callback();
            });
        })
        .catch(err => {
            console.error(err);
        });
}