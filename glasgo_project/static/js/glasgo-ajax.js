$(document).ready(function () {

    var search_input = $("#search-input");
    var search_tags = $(".search-tag");

    // Map the search function to keyup event in the search bar (whenever the text changes)
    search_input.keyup(function () {
        search();
    });
    // Map the search function to click event for the tag checkboxes (whenever a tag is toggled)
    search_tags.click(function () {
        search();
    });

    // Filter attractions with the given search text and tags
    function search() {
        var search = search_input.val();
        var url = search_input.attr("data-url");

        var tags = [];
        search_tags.each(function (i, obj) {
            if ($(this).is(":checked")) {
                tags.push($(this).attr("id"));
            }
        });

        // Send a request to receive the attractions filtered by the given search text and tags
        $.get(
            url,
            {"search": search, "tags": tags},
            function (data) {
                $("#search-results").html(data)
            }
        )
    }

    add_vote_btn_listener();

    // Add vote button event listener for click event
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

            // Send a request to receive the new rating on this attraction
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