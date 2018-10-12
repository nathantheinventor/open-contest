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
                    localStorage.languages = data;
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
            var code = editor.getValue();
            $.post("/submit", {problem: thisProblem, language: language, code: code}, data => {
                if (data != "ok") {
                    alert(data);
                }
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
Contests page
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
            });
        }
        $("#contest-name").keyup(editContest);
        $("#contest-start-date").keyup(editContest);
        $("#contest-start-time").keyup(editContest);
        $("#contest-end-date").keyup(editContest);
        $("#contest-end-time").keyup(editContest);
    }
