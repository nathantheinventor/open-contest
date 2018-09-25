document.addEventListener("visibilitychange", _ => {
    window.setTimeout(_ => {
        window.location.reload();
    }, 500);
}, false);

$(document).ready(function() {
    var editor = ace.edit("ace-editor");
    editor.setShowPrintMargin(false);
    editor.setTheme("ace/theme/chrome");
    function setLanguage() {
        var language = $("select.language-picker").val();
        editor.session.setMode("ace/mode/" + language);
    }
    setLanguage();
    $("select.language-picker").change(setLanguage);
})
