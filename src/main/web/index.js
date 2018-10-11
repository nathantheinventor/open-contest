const { login, logout, submit, getUsers, createUser, deleteUser, getContests, editContest } = require("./callbacks");
const util = require("../util");

exports.serveRequest = (req, res) => {
    const url = req.url;
    if (url == "/logout") {
        return logout(req, res);
    }
    if (req.method != "POST") {
        res.statusCode = 403;
        res.end("POST required");
    }
    if (url == "/login") {
        return login(req, res);
    }
    let user = util.auth.checkUser(req);
    if (user == undefined) {
        res.statusCode = 403;
        res.end("You must be logged in to access this function");
    }
    if (url == "/submit") {
        return submit(req, res);
    } else if (url == "/getUsers") {
        return getUsers(req, res);
    } else if (url == "/createUser") {
        return createUser(req, res);
    } else if (url == "/deleteUser") {
        return deleteUser(req, res);
    } else if (url == "/getContests") {
        return getContests(req, res);
    } else if (url == "/editContest") {
        return editContest(req, res);
    }
    res.statusCode = 404;
    res.end("Not Found");
}
