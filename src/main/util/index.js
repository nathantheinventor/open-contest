exports.files = require("./files");
exports.passwords = require("./passwords");
exports.time = require("./time");
exports.auth = require("./auth");
exports.db = require("./db");

const time = require("./time");

exports.log = data => {
    console.log(`${time.curTimeString()}: ${data}`);
}