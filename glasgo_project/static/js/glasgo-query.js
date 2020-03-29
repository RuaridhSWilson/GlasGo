$(document).ready(function () {

    trim_description_snippets();

    // Add DateTimePickers to starts and ends form fields
    $("#starts").datetimepicker({format: "Y-m-d H:i"});
    $("#ends").datetimepicker({format: "Y-m-d H:i"});

    bsCustomFileInput.init();

    // Map the pad_navbar function to the window resizing and loading events
    $(window).resize(pad_navbar());
    $(window).load(pad_navbar());

    // Create padding below the navbar
    function pad_navbar() {
        $("body").css("padding-top", $("#top-navbar").height() + 10);
    }

    // Make each attraction description brief - take the first 500 characters
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