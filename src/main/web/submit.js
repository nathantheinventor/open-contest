const qs = require('querystring');
const db = require("../../util/db");

async function username(user) {
    const record = await db.getKey(`/users/${user}`);
    return record.username;
}

async function problemName(problem) {
    const record = await db.getKey(`/problems/${problem}/problem.json`);
    return record.title;
}

exports.submit = (req, res) => {
    const user = req.headers.cookie.split("=")[1];
    let body = "";
    req.on("data", data => {
        body += data;
    });
    req.on("end", async _ => {
        const params = qs.parse(body);
        const problem = params.problem;
        const language = params.language;
        const code = params.code;
        console.log(`Submission by ${await username(user)} to problem ${await problemName(problem)} in language ${language}`);
        console.log("---------------------------------------------");
        console.log(code);
        console.log("---------------------------------------------");
    });
}