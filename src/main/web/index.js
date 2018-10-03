const { login } = require("./callbacks");

exports.serveRequest = (req, res) => {
    const url = req.url;
    if (url == "/login") {
        return login(req, res);
    }
    res.statusCode = 404;
    res.end("Not Found");
}