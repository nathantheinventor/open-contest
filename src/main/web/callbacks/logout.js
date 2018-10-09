const util = require("../../util");
const qs = require('querystring');

exports.logout = (req, res) => {
    res.statusCode = 302;
    res.setHeader("Location", "/static/login.html")
    res.setHeader("Set-Cookie", ["user=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT", "userType=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT"]);
    res.end();
}
