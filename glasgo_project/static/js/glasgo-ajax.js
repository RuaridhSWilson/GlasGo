$(document).ready(function () {

    $("#search-input").keyup(function () {
        var search = $(this).val();
        var url = $(this).attr("data-url");

        $.get(url,
            {"search": search},
            function (data) {
                $("#search-results").html(data);
            })
    });

});