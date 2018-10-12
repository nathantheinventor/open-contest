const register = require("../util/register");

register.get("/logout", "any", async (params, headers, setHeader) => {
    setHeader("Location", "/static/login.html")
    setHeader("Set-Cookie", ["user=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT", "userType=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT"]);
    return 302;
});
