const auth = require("./auth");
const qs = require("querystring");

var paths = {};

exports.post = (url, userType, callback) => {
    paths[url + "|POST"] = {
        url: url,
        method: "POST", 
        userType: userType, // any, loggedin, admin, or participant
        callback: callback // callback function
    };
}

exports.get = (url, userType, callback) => {
    paths[url + "|GET"] = {
        url: url,
        method: "GET", 
        userType: userType, // any, loggedin, admin, or participant
        callback: callback // callback function
    };
}

async function fits(req, userType) {
    switch(userType) {
        case "any": return true;
        case "loggedin": return await auth.getUser(req) != undefined;
        case "admin": return await auth.isAdmin(req);
        case "participant": return await auth.isParticipant(req);
    };
}

exports.handleRequest = async (req, res) => {
    const url = req.url;
    const method = req.method;
    if (`${url}|${method}` in paths) {
        const endpoint = paths[`${url}|${method}`];
        if (!await fits(req, endpoint.userType)) {
            if (method == "POST" || await auth.getUser(req) != undefined) {
                res.statusCode = 403;
                res.end("Unauthorized");
            } else {
                res.statusCode = "302";
                res.setHeader("Location", "/static/login.html");
                res.end();
            }
            return
        }
        let body = "";
        req.on('data', data => {
            body += data;
        });
        req.on('end', async _ => {
            const params = qs.parse(body);
            res.statusCode = 200;
            const user = await auth.getUser(req);
            endpoint.callback(params, (header, value) => res.setHeader(header, value), user)
                .then(result => {
                    if (typeof result == "string") {
                        res.setHeader("Content-Type", "text/plain");
                        res.end(result)
                    } else if (typeof result == "number") {
                        res.statusCode = result;
                        res.end();
                    } else {
                        res.setHeader("Content-Type", "application/json");
                        res.end(JSON.stringify(result));
                    }
                })
                .catch(err => {
                    res.statusCode = 500;
                    res.end(err.toString());
                });
        });
    } else {
        res.statusCode = 404;
        res.end("Not found");
    }
}