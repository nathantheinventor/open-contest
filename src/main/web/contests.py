from code.util import register
from code.util.db import Contest

def getContests(params, setHeader, user):
    # return Contest.allJSON()
    return Contest.allJSON()

register.post("/getContests", "loggedin", getContests)

# const util = require("../util");
# const register = require("../util/register");
# const Contest = require("../model").Contest;

# register.post("/getContests", "admin", async _ => {
#     return await Contest.allJSON();
# });

# register.post("/getContest", "admin", async (params) => {
#     const id = params.id;
#     var contest = await Contest.construct(id);
#     return await contest.toJSON();
# });

# register.post("/deleteContest", "admin", async (params) => {
#     const id = params.id;
#     await util.db.deleteKey(`/contests/${id}`);
#     return "ok";
# });

# register.post("/editContest", "admin", async (params) => {
#     const id = params.id;
#     let contest = id ? await Contest.construct(id): new Contest();
    
#     contest.name     = params.name;
#     contest.start    = params.start;
#     contest.end      = params.end;
#     contest.problems = JSON.parse(params.problems);
    
#     await contest.save();

#     return contest.id;
# });
