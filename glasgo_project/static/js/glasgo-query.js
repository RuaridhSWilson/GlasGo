$(document).ready(function () {

    function pad_navbar() {
        $("body").css("padding-top", $("#top-navbar").height()+10);
    }
    $(window).resize(pad_navbar());
    $(window).load(pad_navbar()); // TODO: Figure out why this is causing a TypeError
});