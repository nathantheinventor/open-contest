const util = require("../util");
const Model = require("./model").Model;
const Problem = require("./problem").Problem;

class Contest extends Model {
    static get detailsFile() { return "/contests/{}/contest.json"; }
    get detailsFile() { return "/contests/{}/contest.json"; }
    static get fields() { return ["id", "name", "start", "end", "problems"]; }
    get fields() { return ["id", "name", "start", "end", "problems"]; }
    static get folder() { return "/contests"; }
    constructor() {
        super();
        this.problems = [];
    }
    async save() {
        super.save();
    }
    async getProblems() {
        const ids = this.problems;
        var problems = []
        for (var id of ids) {
            problems.push(await Problem.construct(id));
        }
        return problems;
    }
    async toJSON() {
        let json = super.toJSON();
        const problems = await this.getProblems();
        let jsonProblems = [];
        for (var problem of problems) {
            jsonProblems.push(await problem.toJSON());
        }
        json.problems = jsonProblems;
        return json;
    }
};

exports.Contest = Contest;