const util = require("../util");
const register = require("../util/register");

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
