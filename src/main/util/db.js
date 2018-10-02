const path = require("path");
const files = require("./files");

exports.getKey = async key => {
    const file = path.join("/db", key);
    return JSON.parse(await files.readFile(file));
}

exports.setKey = async (key, value) => {
    const file = path.join("/db", key);
    return await files.writeFile(file, JSON.stringify(value));
}