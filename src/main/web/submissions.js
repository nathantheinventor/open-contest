const util = require("../util");
const register = require("../util/register");

register.get("/submissions", "loggedin", async (_, __, setHeader, user) => {
    setHeader("Location", `/static/submissions/${user.id}.html`);
    return 302;
});