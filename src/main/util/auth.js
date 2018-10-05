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

exports.isAdmin = async req => {
    if (req.headers.cookie == undefined || req.headers.cookie == "" || !req.headers.cookie.indexOf("=") == -1) {
        return false;
    }
    const user = req.headers.cookie.split("=")[1];
    const userdata = await db.getKey(`/users/${user}`);
    return userdata.type = "admin";
}

exports.uuid = _ => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
