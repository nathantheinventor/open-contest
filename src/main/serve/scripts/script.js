// document.addEventListener("visibilitychange", _ => {
//     window.setTimeout(_ => {
//         window.location.reload();
//     }, 500);
// }, false);

/*--------------------------------------------------------------------------------------------------
General page code
--------------------------------------------------------------------------------------------------*/
    function setupHeaderDiv() {
        $("div.header").click(_ => {
            window.location = "/";
        });
    }

    function setupMenu() {
        var userType = "";
        if (document.cookie) {
            userType = document.cookie.split("=")[1];
        }
        $("div.menu-item").each(function() {
            var perms = $(this).attr("role");
            if (perms == "any" || perms == userType) {
                $(this).css("display", "inline-block");
            }
        });
    }

    $(document).ready(function() {
        var pageName = $("h2.page-title").text();
        setupMenu();
        setupLoginButton();
        setupHeaderDiv();
        if ($("#ace-editor").length > 0) {
            setupAceEditor();
            setupSortability();
        }
        if (pageName == "Users") {
            displayExistingUsers();
            setupUserButtons();
        } else if (pageName == "Contests") {
            displayExistingContests();
            setupContestButton();
        } else if (pageName == "Contest") {
            setupContestPage();
        } else if (pageName == "Problems") {
            displayExistingProblems();
            setupProblemButton();
        } else if (pageName == "Problem") {
            setupProblemPage();
        }
    });

/*--------------------------------------------------------------------------------------------------
Problem page
--------------------------------------------------------------------------------------------------*/
    var languages;
    var language;

    async function getLanguages() {
        return new Promise((res, rej) => {
            if (localStorage.languages != undefined) {
                languages = JSON.parse(localStorage.languages);
                res();
            } else {
                $.post("/static/languages.json", {}, data => {
                    localStorage.languages = JSON.stringify(data);
                    languages = JSON.parse(localStorage.languages);
                    res();
                });
            }
        });
    }

    function setupLanguageDropdown() {
        for (var language in languages) {
            $("select.language-picker").append(`<option value="${language}">${languages[language].name}</option>`);
        }
        if (localStorage.language != undefined) {
            $("select.language-picker").val(localStorage.language);
        }
    }

    async function getLanguageDefault(language) {
        return new Promise((res, rej) => {
            if (localStorage[language] != undefined) {
                res(localStorage[language]);
            } else {
                $.post("/static/examples/" + languages[language].example, {}, data => {
                    localStorage[language] = data;
                    res(data);
                });
            }
        });
    }

    function createResultsCard() {
        if ($(".card.results").length == 0) {
            $(".main-content").append(`<div class="results card">
                <div class="card-header">
                    <h2 class="card-title">Results</h2>
                </div>
                <div class="card-contents">
                </div>
            </div>`);
        }
        $(".results.card .card-contents").html(`<div class="results-pending"><i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i></div>`);
    }

    var icons = {
        "ok": "check",
        "wrong_answer": "times",
        "tle": "clock",
        "runtime_error": "exclamation-triangle"
    };

    function showResults(sub) {
        if (sub.results == "compile_error") {
            $(".results.card .card-contents").html(`
                <h3>Compile Error</h3>
                <code>${sub.compile.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;")}</code>
            `);
        } else if (sub.type == "test") {
            var tabs = "";
            var results = "";
            var samples = sub.results.length;
            for (var i = 0; i < samples; i ++) {
                var res = sub.results[i];
                var icon = icons[res];
                tabs += `<li><a href="#tabs-${i}"><i class="fa fa-${icon}" aria-hidden="true"></i> Sample #${i}</a></li>`;

                var input = sub.inputs[i];
                var output = sub.outputs[i];
                var error = sub.errors[i];
                var answer = sub.answers[i];
                var errorStr = `<div class="col-12">
                    <h4>Stderr Output</h4>
                    <code>${error.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;")}</code>
                </div>`;
                if (!error) {
                    errorStr = "";
                }
                results += `<div id="tabs-${i}">
                    <div class="row">
                        <div class="col-12">
                            <h4>Input</h4>
                            <code>${input.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;")}</code>
                        </div>
                        <div class="col-6">
                            <h4>Your Output</h4>
                            <code>${output.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;")}</code>
                        </div>
                        <div class="col-6">
                            <h4>Correct Answer</h4>
                            <code>${answer.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;")}</code>
                        </div>
                        ${errorStr}
                    </div>
                </div>`;
            }
            $(".results.card .card-contents").html(`<div id="result-tabs">
                <ul>
                    ${tabs}
                </ul>
                ${results}
            </div>`);
            $("#result-tabs").tabs();
        }
    }

    async function setupAceEditor() {
        await getLanguages();
        // Get problem ID
        var thisProblem = $("#problem-id").val();

        // Setup ACE editor
        var editor = ace.edit("ace-editor");
        editor.setShowPrintMargin(false);
        editor.setTheme("ace/theme/chrome");

        setupLanguageDropdown();

        // Change the editor when the language changes
        async function setLanguage() {
            language = $("select.language-picker").val();
            localStorage.language = language;
            editor.session.setMode("ace/mode/" + languages[language].aceName);
            if (localStorage[language + "-" + thisProblem] == undefined) {
                localStorage[language + "-" + thisProblem] = await getLanguageDefault(language);
                editor.setValue(localStorage[language + "-" + thisProblem]);
            } else {
                editor.setValue(localStorage[language + "-" + thisProblem]);
            }
        }
        setLanguage();
        $("select.language-picker").change(setLanguage);

        // Save the editor contents to local storage when the editor changes
        editor.session.on('change', delta => {
            localStorage[language + "-" + thisProblem] = editor.getValue();
        });

        // When you click the submit button, submit the code to the server
        $("button.submit-problem").click(_ => {
            createResultsCard();
            var code = editor.getValue();
            $.post("/submit", {problem: thisProblem, language: language, code: code, type: "submit"}, results => {
                showResults(results);
            });
        });

        // When you click the test code button, test the code
        $("button.test-samples").click(_ => {
            createResultsCard();
            var code = editor.getValue();
            $.post("/submit", {problem: thisProblem, language: language, code: code, type: "test"}, results => {
                showResults(results);
            });
        });
    }

    function setupSortability() {
        var thisProblem = $("#problem-id").val();
        if (localStorage["sort-" + thisProblem] != undefined) {
            var order = JSON.parse(localStorage["sort-" + thisProblem]);
            for (var i of [0,1,2,3,4]) {
                var cls = order[i];
                $("div.problem-description").append($("div.problem-description div." + cls))
            }
        }
        $("div.problem-description").sortable({
            placeholder: "ui-state-highlight",
            forcePlaceholderSize: true,
            stop: (event, ui) => {
                var indices = {};
                for (var cls of ["stmt", "inp", "outp", "constraints", "samples"]) {
                    var index = $("div.problem-description > div." + cls).index();
                    indices[index] = cls;
                }
                localStorage["sort-" + thisProblem] = JSON.stringify(indices);
            }
        });
        $("div.problem-description").disableSelection();
    }

/*--------------------------------------------------------------------------------------------------
Login page
--------------------------------------------------------------------------------------------------*/
    function setupLoginButton() {
        $(".login-button").click(_ => {
            var username = $("input[name=username]").val();
            var password = $("input[name=password]").val();
            $.post("/login", {username: username, password: password}, data => {
                if (data == "ok") {
                    window.location = "/static/problems.html";
                } else {
                    alert(data);
                }
            });
        });
    }

/*--------------------------------------------------------------------------------------------------
Users page
--------------------------------------------------------------------------------------------------*/
    function createUserCard(username, password, type) {
        $("div.user-cards").prepend(`<div class="col-3">
            <div class="card${type == "admin" ? " blue": ""}" data-username="${username}">
                <div class="card-header">
                    <strong class="username-hidden"><i>Username:</i></strong><br class="username-hidden"/>
                    <p class="username-hidden">&quot;</p>
                    <h2 class="card-title">${username}</h2>
                    <p class="username-hidden">&quot;</p>
                    <div class="delete-link"><i class="material-icons">clear</i></div>
                </div>
                <div class="card-contents">
                    <strong><i>Password:</i></strong><br/>
                    &quot;${password}&quot;
                </div>
            </div>
        </div>`);
        $(`div[data-username="${username}"] div.delete-link`).click(function() {
            var username = $(this).parents(".card").data("username");
            var col = $(this).parents(".col-3");
            if (confirm(`Are you sure you want to delete ${username}?`)) {
                $.post("/deleteUser", {username: username}, data => {
                    if (data == "ok") {
                        col.remove(); // Bad practice, but I'm not completely sure how to do it right
                    }
                });
            }
        });
    }

    function displayExistingUsers() {
        $.post("/getUsers", {}, data => {
            for (var user of data) {
                createUserCard(user.username, user.password, user.type);
            }
        });
    }

    function setupUserButtons() {
        $("button.create-admin").click(function() {
            var username = prompt("New User's Name")
            if (username) {
                $.post("/createUser", {type: "admin", username: username}, password => {
                    createUserCard(username, password, "admin");
                });
            }
        });
        $("button.create-participant").click(function() {
            var username = prompt("New User's Name")
            if (username) {
                $.post("/createUser", {type: "participant", username: username}, password => {
                    createUserCard(username, password, "participant");
                });
            }
        });
    }

/*--------------------------------------------------------------------------------------------------
Contests page
--------------------------------------------------------------------------------------------------*/
    function createContestCard(contest) {
        $("div.contest-cards").append(`<a href="/static/contest.html#${contest.id}" class="card-link">
            <div class="card" data-contest="${contest.id}" data-name="${contest.name}">
                <div class="card-header">
                    <h2 class="card-title">${contest.name}</h2>
                    <div class="delete-link"><i class="material-icons">clear</i></div>
                </div>
                <div class="card-contents">
                    ${new Date(parseInt(contest.start)).toLocaleString()} - ${new Date(parseInt(contest.end)).toLocaleString()}
                </div>
            </div>
        </a>`);
        $(`div[data-contest="${contest.id}"] div.delete-link`).click(function() {
            var card = $(this).parents(".card");
            var contest = card.data("contest");
            var name = card.data("name");
            if (confirm(`Are you sure you want to delete ${name}?`)) {
                $.post("/deleteContest", {id: contest}, data => {
                    if (data == "ok") {
                        card.remove(); // Bad practice, but I'm not completely sure how to do it right
                    }
                });
            }
            return false;
        });
    }

    function displayExistingContests() {
        $.post("/getContests", {}, contests => {
            for (var contest of contests) {
                createContestCard(contest);
            }
        });
    }

    function setupContestButton() {
        $(".create-contest").click(function() {
            window.location = "/static/contest.html";
        });
    }

/*--------------------------------------------------------------------------------------------------
Contest page
--------------------------------------------------------------------------------------------------*/
    function editContest() {
        var id = (window.location.hash || "#").substr(1);
        var name = $("#contest-name").val();
        var startDate = $("#contest-start-date").val();
        var startTime = $("#contest-start-time").val();
        var endDate = $("#contest-end-date").val();
        var endTime = $("#contest-end-time").val();

        var start = new Date(`${startDate} ${startTime}`);
        var end = new Date(`${endDate} ${endTime}`);

        $.post("/editContest", {id: id, name: name, start: start.getTime(), end: end.getTime()}, id => {
            window.location.hash = id;
        });
    }

    var problemsHere = {};
    function setupContestPage() {
        if (window.location.hash) {
            $.post("/getContest", {id: window.location.hash.substr(1)}, contest => {
                $("#contest-name").val(contest.name);
                var timezone = new Date().getTimezoneOffset() * 60000;
                var start = new Date(parseInt(contest.start) - timezone);
                $("#contest-start-date").val(start.toJSON().slice(0, 10));
                $("#contest-start-time").val(start.toJSON().slice(11, 19));
                var end = new Date(parseInt(contest.end) - timezone);
                $("#contest-end-date").val(end.toJSON().slice(0, 10));
                $("#contest-end-time").val(end.toJSON().slice(11, 19));
                for (var problem of contest.problems) {
                    createProblemCard(problem, true);
                    problemsHere[problem.id] = true;
                }
            });
        }
        $(".contest-details input").keyup(editContest);
        $("button.choose-problem").click(function() {
            $.post("/getProblems", {}, problems => {
                $("select.problem-choice option[value]").remove();
                for (var problem of problems) {
                    if (!problemsHere[problem.id]) {
                        $("select.problem-choice").append(`<option value="${problem.id}">${problem.title}</option>`);
                    }
                }
                $("div.modal").modal();
            });
        });
        $("button.add-problem").click(function() {
            if ($("select.problem-choice").val() != "-") {
                if (!window.location.hash) {
                    alert("You must fill in the contest details before you add a problem");
                }
                var contest = window.location.hash.substr(1);
                var problem = $("select.problem-choice").val();
                $.post("/addContestProblem", {contest: contest, problem: problem}, result => {
                    if (result == "ok") {
                        problemsHere[problem] = true;
                        $.post("/getProblem", {id: problem}, problem => {
                            createProblemCard(problem, true);
                            $("div.modal").modal("hide");
                        });
                    }
                });
            }
        })
    }

/*--------------------------------------------------------------------------------------------------
Problems page
--------------------------------------------------------------------------------------------------*/
    function createProblemCard(problem, contestPage=false) {
        $("div.problem-cards").append(`<div class="card" data-problem="${problem.id}" data-title="${problem.title}">
            <div class="card-header">
                <h2 class="card-title">${problem.title}</h2>
                <div class="delete-link"><i class="material-icons">clear</i></div>
            </div>
            <div class="card-contents">
                ${problem.description}
            </div>
        </div>`);
        if (contestPage) {
            $("div.problem-cards").sortable({
                placeholder: "ui-state-highlight",
                forcePlaceholderSize: true,
                stop: _ => {
                    var order = [];
                    $("div.card").each((_, item) => {
                        if ($(item).data("problem")) {
                            order.push($(item).data("problem"));
                        }
                    });
                    $.post("/setContestOrder", {contest: window.location.hash.substr(1), order: JSON.stringify(order)});
                }
            });
        }
        $("div.card[data-problem]").click(a => {
            window.location = "/static/problem.html#" + $(a.currentTarget).data("problem");
        });
        $(`div[data-problem="${problem.id}"] div.delete-link`).click(function() {
            var card = $(this).parents(".card");
            var problem = card.data("problem");
            var title = card.data("title");
            if (confirm(`Are you sure you want to delete ${title}?`)) {
                var url = contestPage ? "/deleteContestProblem": "/deleteProblem";
                var params = contestPage ? {problem: problem, contest: window.location.hash.substr(1)}: {id: problem};
                if (contestPage) {
                    delete problemsHere[problem];
                }
                $.post(url, params, data => {
                    if (data == "ok") {
                        card.remove(); // Bad practice, but I'm not completely sure how to do it right
                    }
                });
            }
            return false;
        });
    }

    function displayExistingProblems() {
        $.post("/getProblems", {}, problems => {
            for (var problem of problems) {
                createProblemCard(problem);
            }
        });
    }

    function setupProblemButton() {
        $(".create-problem").click(function() {
            window.location = "/static/problem.html";
        });
    }


/*--------------------------------------------------------------------------------------------------
Problem page
--------------------------------------------------------------------------------------------------*/
    function editProblem() {
        var id = (window.location.hash || "#").substr(1);
        problem = {id: id};
        problem.title       = $("#problem-title").val();
        problem.description = $("#problem-description").val();
        problem.statement   = mdEditors[0].value();
        problem.input       = mdEditors[1].value();
        problem.output      = mdEditors[2].value();
        problem.constraints = mdEditors[3].value();
        problem.samples     = $("#problem-samples").val();

        $.post("/editProblem", problem, id => {
            window.location.hash = id;
        });
    }

    var mdEditors = [];
    function setupProblemPage() {
        $(".rich-text textarea").each((_, elem) => {
            mdEditors.push(new SimpleMDE({ element: elem }));
        });
        if (window.location.hash) {
            $.post("/getProblem", {id: window.location.hash.substr(1)}, problem => {
                $("#problem-title").val(problem.title);
                $("#problem-description").val(problem.description);
                mdEditors[0].value(problem.statement);
                mdEditors[1].value(problem.input);
                mdEditors[2].value(problem.output);
                mdEditors[3].value(problem.constraints);
                $("#problem-samples").val(problem.samples);
            });
        }
        $(":input").keyup(editProblem);
    }
