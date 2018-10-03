const db = require("./db");

exports.checkPassword = async (username, password) => {
    const data = await db.getKey(`/users/${username}`);
    if (data == undefined) {
        return false;
    }
    if (data.password == password) {
        return data.id;
    }
    return false;
}

exports.checkUser = req => {
    if (req.headers.cookie == undefined || req.headers.cookie == "" || !req.headers.cookie.indexOf("=") == -1) {
        return undefined;
    }
    return req.headers.cookie.split("=")[1];
}
