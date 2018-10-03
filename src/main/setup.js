const http = require("http");
const fs = require("fs");
const path = require("path");
const util = require("./util");
const web = require("./web");
const uuidv1 = require("uuid/v1");
const { exec } = require("child_process");
const url2 = require("url");

// Get the primary arguments
const args = process.argv;
const primaryUsername = args[2]; // The username of the admin user setting up the server
const port = args[3]; // The port to run the server on

// Generate a four word password for the admin user; i.e. XKCD's "correct horse battery staple"
let adminPassword = util.passwords.password();
adminPassword = "presently description kirk died";
console.log(`The admin password is "${adminPassword}"`);
const adminId = uuidv1();
util.db.setKey(`/users/${primaryUsername}`, {
    password: adminPassword,
    id: adminId
});
util.db.setKey(`/users/${adminId}`, {
    username: primaryUsername
});

// Create the server
const server = http.createServer((req, res) => {
    // When a request comes in, forward it based on the URL
    const url = req.url;
    util.log(`Call to ${url}`)
    
    // Redirect the root to the login page
    if (url == "/") {
        res.statusCode = 302;
        res.setHeader("Location", "/static/login.html");
        res.end();
        return;
    }

    // Serve static files
    if (url.startsWith("/static")) {
        // Get the path to the file to serve
        let file = path.relative("/static", url);
        file = url2.parse(file).pathname;
        file = path.join("/code/serve", file);
        util.log(`Serving file ${file}`);

        // Read the file
        fs.readFile(file, (err, data) => {
            if (err) {
                // The file wasn't found
                res.statusCode = 404;
                res.setHeader("Content-Type", "text/plain");
                res.end(`File not found: ${url}`);
                return;
            }

            // The file was found
            res.statusCode = 200;
            res.end(data);
        });
        return;
    }

    // If it's not a static file, forward the request to the web handler
    web.serveRequest(req, res);
});

// Start serving
server.listen(port, '0.0.0.0', _ => {
    console.log(`Server started at 0.0.0.0:${port}`);
});

exec("killall -9 python3", (err, stdout, stderr) => {
    console.log(stdout);
    console.error(stderr)
});

exec("python3 /code/setup.py", (err, stdout, stderr) => {
    console.log(stdout);
    console.error(stderr)
});
