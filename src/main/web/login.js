const util = require("../util");
const register = require("../util/register");

register.post("/login", "any", async (params, headers, setHeader) => {
    const username = params.username;
    const password = params.password;
    const user = await util.auth.checkPassword(username, password);
    if (user) {
        setHeader("Set-Cookie", [`user=${user.id}; HttpOnly`, `userType=${user.type}`]);
        return "ok";
    } else {
        return "Incorrect username / password";
    }
});
