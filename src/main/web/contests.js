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

register.post("/getContest", "admin", async (params) => {
    const id = params.id;
    return await util.db.getKey(`/contests/${id}/contest.json`);
});

register.post("/deleteContest", "admin", async (params) => {
    const contestId = params.id;
    util.db.deleteKey(`/contests/${contestId}`);
    return "ok";
});

register.post("/editContest", "admin", async (params) => {
    let id = params.id;
    const name = params.name;
    const start = params.start;
    const end = params.end;
    if (id == "") {
        id = util.auth.uuid();
    }
    console.log(id, name, start, end);
    await util.db.setKey(`/contests/${id}/contest.json`, {
        id: id,
        name: name,
        start: start,
        end: end
    });
    return id;
});
