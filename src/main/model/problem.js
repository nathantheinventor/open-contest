const util = require("../util");
const Model = require("./model").Model;

class Datum {
    static async construct(id, num) {
        var d = new Datum();
        d.input = await util.db.getKey(`/problems/${id}/input/in${num}.txt`);
        d.answer = await util.db.getKey(`/problems/${id}/output/out${num}.txt`);
        return d;
    }
    toJSON() {
        return {
            input: this.input,
            output: this.output
        }
    }
}

class Problem extends Model {
    static get detailsFile() { return "/problems/{}/problem.json"; }
    get detailsFile() { return "/problems/{}/problem.json"; }
    static get fields() { return ["id", "title", "description", "statement", "input", "output", "constraints", "samples", "tests"]; }
    get fields() { return ["id", "title", "description", "statement", "input", "output", "constraints", "samples", "tests"]; }
    static get folder() { return "/problems"; }
    async getSampleData() {
        let samples = [];
        for (var i = 0; i < this.samples; i ++) {
            samples.push(await Datum.construct(this.id, i));
        }
        return samples;
    }
    async getTestData() {
        let tests = [];
        for (var i = 0; i < this.tests; i ++) {
            tests.push(await Datum.construct(this.id, i));
        }
        return tests;
    }
    async toJSON() {
        let json = super.toJSON();
        const sampleData = await this.getSampleData();
        json.sampleData = sampleData.map(datum => datum.toJSON());
        return json;
    }
};

exports.Problem = Problem;