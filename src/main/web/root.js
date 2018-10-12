const register = require("../util/register");

register.get("/", "loggedin", async (_, ___, setHeader) => {
    setHeader("Location", `/static/problems.html`);
    return 302;
});
