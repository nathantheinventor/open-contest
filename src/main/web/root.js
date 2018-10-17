const register = require("../util/register");

register.get("/", "loggedin", async (_, setHeader) => {
    setHeader("Location", `/static/problems.html`);
    return 302;
});
