const path = require("path");
const files = require("./files");

exports.getKey = async key => {
    const file = path.join("/db", key);
    try {
        const contents = await files.readFile(file);
        if (contents.startsWith("{") || contents.startsWith("[")) {
            return JSON.parse(contents);
        }
        return contents;
    } catch (err) {
        console.error(`Error with file ${file}: ${err}`)
        return undefined;
    }
}

exports.setKey = async (key, value) => {
    files.ensureExists(path.join("/db", key));
    const file = path.join("/db", key);
    return await files.writeFile(file, JSON.stringify(value));
}

exports.deleteKey = async key => {
    try {
        const file = path.join("/db", key);
        return await files.deleteFile(file);
    } catch (err) {
        return;
    }
}

exports.listSubKeys = async key => {
    files.ensureExists(path.join("/db", key, "a"));
    const dir = path.join("/db", key);
    const contents = await files.listDir(dir);
    return contents;
}
