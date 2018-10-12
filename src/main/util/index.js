exports.files = require("./files");
exports.passwords = require("./passwords");
exports.time = require("./time");
exports.auth = require("./auth");
exports.db = require("./db");
exports.register = require("./register");

const time = require("./time");

exports.log = data => {
    console.log(`${time.curTimeString()}: ${data}`);
}