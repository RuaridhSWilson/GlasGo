$(document).ready(function () {

    jQuery.validator.setDefaults({
        debug: false,
        success: "valid",
    });

    // Returns true (valid) if the entered username contains no special characters
    jQuery.validator.addMethod("username_chars", function (value, element) {
        return /^[a-zA-Z0-9_]+$/.test(value);
    });

    // Returns true (valid) if no dates were chosen or if the End Date is after the Start Date
    jQuery.validator.addMethod("ends_after_start", function (value, element, starts) {
        if (value.length > 0 && $(starts).val().length > 0) {
            return new Date(value) > new Date($(starts).val());
        } else {
            return true;
        }
    });

    // Validate the Login form:
    // Username is required, must be at most 30 characters and contain no special characters
    // Password is required
    $("form[name='login']").validate({
        rules: {
            username: {
                required: true,
                maxlength: 30,
                username_chars: true,
            },
            password: "required"
        },
        messages: {
            username: {
                required: "Enter your username",
                maxlength: "Too long",
                username_chars: "Invalid characters",
            },
            password: "Enter your password"
        },
        submitHandler: function (form) {
            form.submit();
        }
    });

    // Validate the Register form:
    // Username is required, must be at most 30 characters and contain no special characters
    // Email must be a valid email address and at most 75 characters
    // Password is required and must be between 6 and 128 characters
    // Confirm Password is required and must match the Password
    $("form[name='register']").validate({
        rules: {
            username: {
                required: true,
                maxlength: 30,
                username_chars: true,
            },
            email: {
                required: false,
                maxlength: 75,
                email: true,
            },
            password1: {
                required: true,
                minlength: 6,
                maxlength: 128,
            },
            password2: {
                required: true,
                equalTo: "#password1",
            }
        },
        messages: {
            username: {
                required: "Enter a username",
                maxlength: "Maximum 30 characters",
                username_chars: "Alphanumeric characters only",
            },
            email: {
                maxlength: "Maximum 75 characters",
                email: "Invalid email address",
            },
            password1: {
                required: "Enter a password",
                minlength: "Minimum 6 characters",
                maxlength: "Maximum 128 characters",
            },
            password2: {
                required: "Repeat your password",
                equalTo: "Passwords don't match",
            },
        },
        submitHandler: function (form) {
            form.submit();
        }
    });

    // Validate the Change Password form:
    // Old Password is required
    // New Password is required and must be between 6 and 128 characters
    // Confirm New Password is required and must match the New Password
    $("form[name='password_change']").validate({
        rules: {
            old_password: {
                required: true,
            },
            new_password1: {
                required: true,
                minlength: 6,
                maxlength: 128,
            },
            new_password2: {
                required: true,
                equalTo: "#new_password1",
            }
        },
        messages: {
            old_password: {
                required: "Enter your old password",
            },
            new_password1: {
                required: "Enter your new password",
                minlength: "Minimum 6 characters",
                maxlength: "Maximum 128 characters",
            },
            new_password2: {
                required: "Repeat your password",
                equalTo: "Passwords don't match",
            },
        },
        submitHandler: function (form) {
            form.submit();
        }
    });

    // Validate the Add Attraction form:
    // Title is required and must be at most 128 characters
    // Link must be a valid URL
    // Image is required
    // Description is required
    // Location is required
    // Start Date must be a valid date
    // End Date must be a valid date and must be later than the Start Date
    $("form[name='add_attraction']").validate({
        rules: {
            title: {
                required: true,
                maxlength: 128,
            },
            link: {
                url: true,
            },
            image: {
                required: true,
            },
            description: {
                required: true,
            },
            location: {
                required: true,
            },
            starts: {
                date: true,
            },
            ends: {
                date: true,
                ends_after_start: "#starts",
            },
        },
        messages: {
            title: {
                required: "Enter the attraction title",
                maxlength: "Maximum 128 characters",
            },
            link: {
                url: "Invalid URL",
            },
            image: {
                required: "Add an image",
            },
            description: {
                required: "Describe the attraction",
            },
            location: {
                required: "Provide an address",
            },
            starts: {
                date: "Invalid date",
            },
            ends: {
                date: "Invalid date",
                ends_after_start: "End date is before start date",
            },
        },
        submitHandler: function (form) {
            form.submit();
        }
    });

});