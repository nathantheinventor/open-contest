const util = require("../util");
const register = require("../util/register");

register.post("/getUsers", "admin", async _ => {
    const users = await util.db.listSubKeys("/users");
    const checker = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    let userList = [];
    for (const user of users) {
        if (!checker.test(user)) {
            userList.push(await util.db.getKey(`/users/${user}`));
            console.log(`Adding user ${user}`)
        }
    }
    return userList;
});

register.post("/createUser", "admin", async (params) => {
    const newPassword = util.passwords.password();
    const newGuid = util.auth.uuid();
    const user = {
        username: params.username,
        password: newPassword,
        id: newGuid,
        type: params.type
    }
    await util.db.setKey(`/users/${params.username}`, user);
    await util.db.setKey(`/users/${newGuid}`, user);
    return newPassword;
});

register.post("/deleteUser", "admin", async (params) => {
    const user = await util.db.getKey(`/users/${params.username}`);
    await util.db.deleteKey(`/users/${user.username}`);
    await util.db.deleteKey(`/users/${user.id}`);
    return "ok";
});
