const db = require("./db");

exports.checkPassword = async (username, password) => {
    const data = await db.getKey(`/users/${username}`);
    if (data == undefined) {
        return false;
    }
    if (data.password == password) {
        return true;
    }
    return false;
}
