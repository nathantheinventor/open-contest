const { login } = require("./callbacks");
const util = require("../util");

exports.serveRequest = (req, res) => {
    const url = req.url;
    if (req.method != "POST") {
        req.statusCode = 403;
        req.end("POST required");
    }
    if (url == "/login") {
        return login(req, res);
    }
    let user = util.auth.checkUser(req);
    if (user == undefined) {
        req.statusCode = 403;
        req.end("You must be logged in to access this function");
    }
    res.statusCode = 404;
    res.end("Not Found");
}
