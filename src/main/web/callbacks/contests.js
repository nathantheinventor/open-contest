const util = require("../../util");
const register = require("../../util/register");
const db = require("../../util/db");

register.post("/getContests", "admin", async _ => {
    const contestIds = await util.db.listSubKeys("/contests");
    let contests = [];
    for (var id of contestIds) {
        contests.push(await util.db.getKey(`/contests/${id}/contest.json`));
    }
    return contests;
});

register.post("/deleteContest", "admin", async (params) => {
    const contestId = await params.id;
    util.db.deleteKey(`/contests/${contestId}`);
    return "ok";
});


exports.getContests = async (req, res) => {
    if (util.auth.isAdmin(req)) {
        const contestIds = await util.db.listSubKeys("/contests");
        let contests = [];
        for (var id of contestIds) {
            contests.push(await util.db.getKey(`/contests/${id}/contest.json`));
        }
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(contests));
    } else {
        res.statusCode = 403;
        res.end("Unauthorized");
    }
}

exports.deleteContest = async (req, res) => {
    if (util.auth.isAdmin(req)) {
        const contest = "";
        const contestIds = await util.db.listSubKeys("/contests");
        let contests = [];
        for (var id of contestIds) {
            contests.push(await util.db.getKey(`/contests/${id}/contest.json`));
        }
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(contests));
    } else {
        res.statusCode = 403;
        res.end("Unauthorized");
    }
}

exports.editContest = (req, res) => {
    ;
}
