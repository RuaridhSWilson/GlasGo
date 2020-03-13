$(document).ready(function () {

    var search_input = $("#search-input");
    var search_tags = $(".search-tag");

    search_input.keyup(function () {
        search();
    });
    search_tags.click(function () {
        search();
    });

    function search() {
        var search = search_input.val();
        var url = search_input.attr("data-url");

        var tags = [];
        search_tags.each(function (i, obj) {
            if ($(this).is(":checked")) {
                tags.push($(this).attr("id"));
            }
        });

        $.get(
            url,
            {"search": search, "tags": tags},
            function (data) {
                $("#search-results").html(data)
            }
        )
    }

    add_vote_btn_listener();

    function add_vote_btn_listener() {
        $(".vote-btn").click(function () {
            var attraction = $(this).attr("data-attraction");
            var user = $(this).attr("data-user");
            var like = $(this).attr("data-like");
            var url = $(this).attr("data-url");

            var classes = this.classList;
            if (classes[classes.length - 1] === "active") {
                like = "None"
            }

            $.get(
                url,
                {"attraction": attraction, "user": user, "like": like},
                function (data) {
                    $("#rating").html(data);
                    add_vote_btn_listener();
                });
        });
    }

});