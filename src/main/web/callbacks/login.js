const util = require("../../util");
const qs = require('querystring');

exports.login = (req, res) => {
    if (req.method != "POST") {
        throw new Error("POST method required for /login");
    }
    let body = "";
    req.on('data', data => {
        body += data;
    });
    req.on('end', async _ => {
        params = qs.parse(body)
        const username = params.username;
        const password = params.password;
        const user = await util.auth.checkPassword(username, password);
        if (user) {
            res.statusCode = 200;
            res.setHeader("Set-Cookie", `user=${user}; Secure; HttpOnly`);
            res.end("ok");
        } else {
            res.statusCode = 200;
            res.end("Incorrect username / password")
        }
    });
}
