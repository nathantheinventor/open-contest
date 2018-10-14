const util = require("../util");
const register = require("../util/register");
const Contest = require("../model").Contest;

register.post("/getContests", "admin", async _ => {
    return await Contest.allJSON();
});

register.post("/getContest", "admin", async (params) => {
    const id = params.id;
    var contest = await Contest.construct(id);
    return await contest.toJSON();
});

register.post("/deleteContest", "admin", async (params) => {
    const id = params.id;
    await util.db.deleteKey(`/contests/${id}`);
    return "ok";
});

register.post("/editContest", "admin", async (params) => {
    const id = params.id;
    let contest = id ? await Contest.construct(id): new Contest();
    
    contest.name = params.name;
    contest.start = params.start;
    contest.end = params.end;
    
    await contest.save();

    return contest.id;
});

register.post("/addContestProblem", "admin", async (params) => {
    const contestId = params.contest;
    const problemId = params.problem;
    
    let contest = await Contest.construct(contestId);
    contest.problems.push(problemId);
    contest.save();

    return "ok";
});

register.post("/deleteContestProblem", "admin", async (params) => {
    const contestId = params.contest;
    const problemId = params.problem;
    
    let contest = await Contest.construct(contestId);
    contest.problems = contest.problems.filter(id => id != problemId);
    contest.save();

    return "ok";
});

register.post("/setContestOrder", "admin", async (params) => {
    const contestId = params.contest;
    const order = JSON.parse(params.order);
    
    let contest = await Contest.construct(contestId);
    contest.problems = order;
    contest.save();

    return "ok";
});
