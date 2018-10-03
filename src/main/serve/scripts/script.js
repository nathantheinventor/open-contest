// document.addEventListener("visibilitychange", _ => {
//     window.setTimeout(_ => {
//         window.location.reload();
//     }, 500);
// }, false);

function setupAceEditor () {
    if ($("#ace-editor").length > 0) {
        var editor = ace.edit("ace-editor");
        editor.setShowPrintMargin(false);
        editor.setTheme("ace/theme/chrome");
        function setLanguage() {
            var language = $("select.language-picker").val();
            editor.session.setMode("ace/mode/" + language);
        }
        setLanguage();
        $("select.language-picker").change(setLanguage);
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
});
