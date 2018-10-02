const http = require("http");
const fs = require("fs");
const path = require("path");
const util = require("./util");
const web = require("./web");
const uuidv1 = require("uuid/v1");

// Get the primary arguments
const args = process.argv;
const primaryUsername = args[2]; // The username of the admin user setting up the server
const port = args[3]; // The port to run the server on

// Generate a four word password for the admin user; i.e. XKCD's "correct horse battery staple"
const adminPassword = util.passwords.password();
console.log(`The admin password is "${adminPassword}"`);
util.db.setKey(`/users/${primaryUsername}`, {
    password: adminPassword,
    id: uuidv1()
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
