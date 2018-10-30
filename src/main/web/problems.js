const util = require("../util");
const register = require("../util/register");
const Problem = require("../model").Problem;

register.post("/getProblems", "admin", async _ => {
    return await Problem.allJSON();
});

register.post("/getProblem", "admin", async (params) => {
    const id = params.id;
    var problem = await Problem.construct(id);
    return await problem.toJSONFull();
});

register.post("/deleteProblem", "admin", async (params) => {
    const id = params.id;
    await util.db.deleteKey(`/problems/${id}`);
    return "ok";
});

register.post("/editProblem", "admin", async (params) => {
    const id = params.id;
    let problem = id ? await Problem.construct(id): new Problem();
    
    problem.title       = params.title;
    problem.description = params.description;
    problem.statement   = params.statement;
    problem.input       = params.input;
    problem.output      = params.output;
    problem.constraints = params.constraints;
    problem.samples     = params.samples;
    problem.tests       = 0;

    await problem.save();

    return problem.id;
});
