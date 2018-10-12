const util = require("../../util");
const qs = require("querystring");

exports.getUsers = async (req, res) => {
    if (await util.auth.isAdmin(req)) {
        const users = await util.db.listSubKeys("/users");
        const checker = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
        let userList = [];
        for (const user of users) {
            if (!checker.test(user)) {
                userList.push(await util.db.getKey(`/users/${user}`));
                console.log(`Adding user ${user}`)
            }
        }
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(userList));
    } else {
        res.statusCode = 403;
        res.end("Not Admin");
    }
}

async function getParams(req) {
    return new Promise((res, rej) => {
        let body = "";
        req.on('data', data => {
            body += data;
        });
        req.on('end', async _ => {
            const params = qs.parse(body);
            res(params);
        });
    });
}

exports.createUser = async (req, res) => {
    if (await util.auth.isAdmin(req)) {
        const params = await getParams(req);
        const newPassword = util.passwords.password();
        const newGuid = util.auth.uuid();
        const user = {
            username: params.username,
            password: newPassword,
            id: newGuid,
            type: params.type
        }
        util.db.setKey(`/users/${params.username}`, user);
        util.db.setKey(`/users/${newGuid}`, user);
        res.statusCode = 200;
        res.end(newPassword);
    } else {
        res.statusCode = 403;
        res.end("Not Admin");
    }
}

exports.deleteUser = async (req, res) => {
    if (await util.auth.isAdmin(req)) {
        const params = await getParams(req);
        const user = await util.db.getKey(`/users/${params.username}`);
        util.db.deleteKey(`/users/${user.username}`);
        util.db.deleteKey(`/users/${user.id}`);
        res.statusCode = 200;
        res.end("ok");
    } else {
        res.statusCode = 403;
        res.end("Not Admin");
    }
}
