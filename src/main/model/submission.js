const util = require("../util");
const Model = require("./model").Model;
const Problem = require("./problem").Problem;

class Submission extends Model {
    static get detailsFile() { return "/submissions/{}/submission.json"; }
    get detailsFile() { return "/submissions/{}/submission.json"; }
    static get fields() { return ["id", "user", "problem", "timestamp", "language", "code", "type", "results"]; }
    get fields() { return ["id", "user", "problem", "timestamp", "language", "code", "type", "results", "inputs", "outputs", "errors", "answers", "compile"]; }
    static get folder() { return "/submissions"; }
    constructor() {
        super();
    }
    async getProblem() {
        return await Problem.construct(this.problem);
    }
};

exports.Submission = Submission;