// const http = require("http");
// const fs = require("fs");
// const path = require("path");
// const util = require("./util");
// require("./web");
const { exec } = require("child_process");
// const url2 = require("url");

// // Get the primary arguments
const args = process.argv;
const primaryUsername = args[2]; // The username of the admin user setting up the server
const port = args[3]; // The port to run the server on

// // Generate a four word password for the admin user; i.e. XKCD's "correct horse battery staple"
// let adminPassword = util.passwords.password();
// adminPassword = "presently description kirk died"; // TODO: remove this
// console.log(`The admin password is "${adminPassword}"`);
// let adminId = util.auth.uuid();
// adminId = "286030a0-c74a-11e8-9e2c-83267e901a62"; // TODO: remove this
// util.db.setKey(`/users/${primaryUsername}`, {
//     username: primaryUsername,
//     password: adminPassword,
//     id: adminId,
//     type: "admin"
// });
// util.db.setKey(`/users/${adminId}`, {
//     username: primaryUsername,
//     password: adminPassword,
//     id: adminId,
//     type: "admin"
// });

// const extensions = {
//     ".css": "text/css",
//     ".js": "text/javascript",
//     ".html": "text/html",
//     ".json": "application/json"
// }

// function mimeType(file) {
//     for (var extension in extensions) {
//         if (file.endsWith(extension)) {
//             return extensions[extension];
//         }
//     }
//     return "text/plain";
// }

// // Create the server
// const server = http.createServer((req, res) => {
//     // When a request comes in, forward it based on the URL
//     const url = req.url;
//     util.log(`Call to ${url}`)
    
//     // Serve static files
//     if (url.startsWith("/static")) {
//         // Get the path to the file to serve
//         let file = path.relative("/static", url);
//         file = url2.parse(file).pathname;
//         file = path.join("/code/serve", file);
//         util.log(`Serving file ${file}`);

//         // Read the file
//         fs.readFile(file, (err, data) => {
//             if (err) {
//                 // The file wasn't found
//                 res.statusCode = 404;
//                 res.setHeader("Content-Type", "text/plain");
//                 res.end(`File not found: ${url}`);
//                 return;
//             }

//             // The file was found
//             res.statusCode = 200;
//             res.setHeader("Content-Type", mimeType(file));
//             res.end(data);
//         });
//         return;
//     }

//     util.register.handleRequest(req, res);
//     // If it's not a static file, forward the request to the web handler
//     // web.serveRequest(req, res);
// });

// // Start serving
// server.listen(port, '0.0.0.0', _ => {
//     console.log(`Server started at 0.0.0.0:${port}`);
// });

function runPython() {
    exec(`python3 /code/setup.py "${primaryUsername}" ${port}`, (_, stdout, stderr) => {
        if (stdout) { console.log(stdout); }
        if (stderr) { console.log(stderr); }
        setTimeout(runPython, 1000);
    });    
}
runPython();
