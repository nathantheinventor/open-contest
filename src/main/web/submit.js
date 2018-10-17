const util = require("../util");
const register = require("../util/register");
const Submission = require("../model/submission").Submission;
const { exec } = require("child_process");

async function addSubmission(prob, lang, code, user, type) {
    let sub = new Submission();
    sub.problem = prob;
    sub.language = lang;
    sub.code = code;
    sub.results = ["pending"];
    sub.user = user;
    sub.timestamp = new Date().getTime();
    sub.type = type;
    await sub.save();
    return sub;
}

const exts = {
    "c": "c",
    "cpp": "cpp",
    "cs": "cs",
    "java": "java",
    "python2": "py",
    "python3": "py",
    "ruby": "rb",
    "vb": "vb"
};

async function readFile(filename) {
    try {
        return (await util.files.readFile(filename)).toString();
    } catch(err) {
        return undefined;
    }
}

async function runCode(sub) {
    const ext = exts[sub.language];
    await util.files.writeFile(`/tmp/${sub.id}/code.${ext}`, sub.code);
    var prob = await sub.getProblem();
    var tests = 0;
    if (sub.type == "test") {
        // Just run the sample data
        tests = prob.samples;
    } else {
        // Run all the tests
        tests = prob.tests;
    }
    for (var i = 0; i < tests; i ++) {
        var input = await util.db.getKey(`/problems/${sub.problem}/input/in${i}.txt`);
        await util.files.writeFile(`/tmp/${sub.id}/in${i}.txt`, input);
    }
    await util.files.writeFile(`/tmp/${sub.id}/out/tmp`, ""); // Create the "out" directory
    return new Promise((res, rej) => {
        exec(`docker run --network=none -m 256MB -v /tmp/${sub.id}/:/source nathantheinventor/open-contest-dev-${sub.language}-runner ${tests} 5`, async (err, stdout, stderr) => {
            if (err) rej(err);
            if (stdout) console.log(stdout);
            if (stderr) console.error(stderr);
            let inputs = [];
            let outputs = [];
            let answers = [];
            let errors = [];
            let results = [];
            let result = "ok";
            for (var i = 0; i < tests; i ++) {
                inputs.push(await readFile(`/tmp/${sub.id}/in${i}.txt`));
                errors.push(await readFile(`/tmp/${sub.id}/out/err${i}.txt`));
                let out = await readFile(`/tmp/${sub.id}/out/out${i}.txt`);
                let ans = await readFile(`/db/problems/${prob.id}/output/out${i}.txt`);
                let res = await readFile(`/tmp/${sub.id}/out/result${i}.txt`);
                outputs.push(out);
                answers.push(ans);
                if (res == "ok" && ans.trim() != out.trim()) {
                    res = "wrong_answer";
                }
                if (res == undefined) {
                    res = "tle";
                }
                results.push(res);
                if (res != "ok" && result == "ok") {
                    result = res;
                }
            }
            sub.result = result;
            if (stdout == "compile_error\n") {
                sub.results = "compile_error";
                sub.compile = await readFile(`/tmp/${sub.id}/out/compile_error.txt`);
            } else {
                if (sub.type == "test") {
                    sub.inputs = inputs;
                    sub.outputs = outputs;
                    sub.answers = answers;
                    sub.errors = errors;
                }
                sub.results = results;
            }
            sub.save();
            await util.files.deleteFile(`/tmp/${sub.id}`);
            res(sub);
        });
    });
}

register.post("/submit", "loggedin", async (params, _, user) => {
    const problemId = params.problem;
    const language = params.language;
    const code = params.code;
    const type = params.type;
    submission = await addSubmission(problemId, language, code, user.id, type);
    return await runCode(submission);
});
