$(document).ready(function () {

    trim_description_snippets();

    $("#starts").datetimepicker({format: "Y-m-d H:i"});
    $("#ends").datetimepicker({format: "Y-m-d H:i"});

    bsCustomFileInput.init();

    $(window).resize(pad_navbar());
    $(window).load(pad_navbar()); // TODO: Figure out why this is causing a TypeError


    function pad_navbar() {
        $("body").css("padding-top", $("#top-navbar").height() + 10);
    }

    function trim_description_snippets() {
        var max_chars = 500;
        var text;
        $(".description-snippet").each(function () {
            text = String($(this).html());
            text = (text.length <= max_chars) ? text : text.substring(0, (max_chars + 1)) + "...";
            $(this).html(text);
        });
    }

});