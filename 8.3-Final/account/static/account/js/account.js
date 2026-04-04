function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i += 1) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

function renderErrors(errors) {
    const $errors = $("#errors");
    $errors.empty();

    if (!errors) {
        return;
    }

    const $alert = $("<div></div>").addClass("alert alert-danger mb-0");
    const $title = $("<p></p>").addClass("mb-2 fw-semibold").text("Please fix the following errors:");
    const $list = $("<ul></ul>").addClass("mb-0");

    Object.keys(errors).forEach(function (field) {
        const fieldLabel = field === "__all__" ? "General" : field;
        errors[field].forEach(function (message) {
            $list.append($("<li></li>").text(`${fieldLabel}: ${message}`));
        });
    });

    $alert.append($title, $list);
    $errors.append($alert);
}

function showLoggedState(username) {
    $("#errors").empty();
    $("#login-section").hide();
    $("#logged-text").text(`Logged as ${username}`);
    $("#logged-section").show();
}

function showLoggedOutState() {
    $("#errors").empty();
    $("#logged-section").hide();
    $("#login-form")[0].reset();
    $("#login-section").show();
}

$(function () {
    $("#login-form").on("submit", function (event) {
        event.preventDefault();

        const payload = {
            username: $("#id_username").val(),
            password: $("#id_password").val()
        };

        $.ajax({
            url: window.ACCOUNT_URLS.login,
            type: "POST",
            data: payload,
            success: function (response) {
                showLoggedState(response.username);
            },
            error: function (xhr) {
                const payload = xhr.responseJSON || {};
                renderErrors(payload.errors || { "__all__": ["Login failed"] });
            }
        });
    });

    $("#logout-btn").on("click", function () {
        $.ajax({
            url: window.ACCOUNT_URLS.logout,
            type: "POST",
            success: function () {
                showLoggedOutState();
            },
            error: function () {
                renderErrors({ "__all__": ["Logout failed"] });
            }
        });
    });
});