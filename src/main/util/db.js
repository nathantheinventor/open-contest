const path = require("path");
const files = require("./files");

exports.getKey = async key => {
    const file = path.join("/db", key);
    try {
        const contents = await files.readFile(file);
        return JSON.parse(contents);
    } catch (err) {
        return undefined;
    }
}

exports.setKey = async (key, value) => {
    const file = path.join("/db", key);
    return await files.writeFile(file, JSON.stringify(value));
}
