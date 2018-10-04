// document.addEventListener("visibilitychange", _ => {
//     window.setTimeout(_ => {
//         window.location.reload();
//     }, 500);
// }, false);

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
    if ($("#ace-editor").length > 0) {
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
}

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

function setupHeaderDiv() {
    $("div.header").click(_ => {
        window.location = "/";
    });
}

$(document).ready(function() {
    setupAceEditor();
    setupLoginButton();
    setupHeaderDiv();
    ;
});
