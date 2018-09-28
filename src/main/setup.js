const http = require("http");
const { passwordGenerator } = require("./web");

const args = process.argv;
const primaryUsername = args[1];
const port = args[2];

const adminPassword = passwordGenerator();
console.log(`The admin password is "${adminPassword}"`);

const server = http.createServer((req, res) => {
    ;
});

server.listen(port);
