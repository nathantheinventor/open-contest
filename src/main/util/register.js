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

function fits(req, userType) {
    switch(userType) {
        case "any": return true;
        case "loggedin": return auth.checkUser(req) != undefined;
        case "admin": return auth.isAdmin(req);
        case "participant": return auth.isParticipant(req);
    };
}

exports.handleRequest = async (req, res) => {
    const url = req.url;
    const method = req.method;
    if (`${url}|${method}` in paths) {
        const endpoint = paths[`${url}|${method}`];
        if (!fits(req, endpoint.userType)) {
            res.statusCode = 403;
            res.end("Unauthorized");
            return
        }
        let body = "";
        req.on('data', data => {
            body += data;
        });
        req.on('end', async _ => {
            const params = qs.parse(body);
            res.statusCode = 200;
            endpoint.callback(params, req.headers, req.setHeader)
                .then(result => {
                    if (typeof result == "string") {
                        res.setHeader("Content-Type", "text/plain");
                        res.end(result)
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