$(document).ready(function () {

    $("#search-input").keyup(function () {
        var search = $(this).val();
        var url = $(this).attr("data-url");

        $.get(url,
            {"search": search},
            function (data) {
                $("#search-results").html(data);
            });
    });

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

            $.get(url,
                {"attraction": attraction, "user": user, "like": like},
                function (data) {
                    $("#rating").html(data);
                    add_vote_btn_listener();
                });
        });
    }

});