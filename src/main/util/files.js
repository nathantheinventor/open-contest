const fs = require("fs");

exports.writeFile = async (filename, contents) => {
    return new Promise((res, rej) => {
        fs.writeFile(filename, contents, err => {
            if (err) {
                rej(err);
            } else {
                res();
            }
        });
    });
}

exports.readFile = async filename => {
    return new Promise((res, rej) => {
        fs.readFile(filename, (err, data) => {
            if (err) {
                rej(err);
            } else {
                res(data);
            }
        });
    });
}

exports.deleteFile = async filename => {
    return new Promise((res, rej) => {
        fs.stat(filename, (err, stats) => {
            if (err) {
                rej(err); return;
            }
            if (stats.isDirectory()) {
                fs.rmdir(filename, err => {
                    if (err) {
                        rej(err); return;
                    }
                    res();
                });
            } else {
                fs.unlink(filename, err => {
                    if (err) {
                        rej(err); return;
                    }
                    res();
                });
            }
        });
        fs.readFile(filename, (err, data) => {
            if (err) {
                rej(err);
            } else {
                res(data);
            }
        });
    });
}

exports.listDir = async dirname => {
    return new Promise((res, rej) => {
        fs.readdir(dirname, (err, files) => {
            if (err) {
                rej(err);
            } else {
                let newList = [];
                for (var file of files) {
                    if (!file.startsWith(".")) {
                        newList.push(file);
                    }
                }
                res(newList);
            }
        });
    });
}
