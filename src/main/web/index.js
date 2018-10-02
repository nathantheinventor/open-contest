const { login } = require("./callbacks");

exports.serveRequest = (req, res) => {
    const url = req.url;
    if (url == "/login") {
        login(req, res);
    }
}