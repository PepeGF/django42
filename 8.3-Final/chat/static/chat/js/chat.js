$(function () {
    const roomName = window.CHAT_CONFIG.roomName;
    const wsScheme = window.CHAT_CONFIG.wsScheme;
    const currentUsername = window.CHAT_CONFIG.currentUsername;

    const chatSocket = new WebSocket(
    wsScheme + "://" + window.location.host + "/ws/chat/" + encodeURIComponent(roomName) + "/"
);

    function scrollToBottom() {
        const container = document.getElementById("messages-container");
        container.scrollTop = container.scrollHeight;
    }

    function appendMessage(username, message) {
        const $row = $("<div></div>").addClass("mb-2");
        const $item = $("<div></div>")
            .addClass("alert py-2 px-3 mb-0")
            .append($("<strong></strong>").text(username + ": "))
            .append(document.createTextNode(message));

        if (username === "system") {
            $item.addClass("alert-info");
        } else if (username === currentUsername) {
            $item.addClass("alert-success");
        } else {
            $item.addClass("alert-light border");
        }

        $row.append($item);
        $("#messages-container").append($row);
        scrollToBottom();
    }

    function renderUserList(users) {
        const $userList = $("#user-list");
        $userList.empty();

        users.forEach(function (username) {
            const $item = $("<li></li>")
                .addClass("list-group-item d-flex justify-content-between align-items-center")
                .text(username);

            if (username === currentUsername) {
                $item.append(
                    $("<span></span>")
                        .addClass("badge text-bg-primary rounded-pill")
                        .text("you")
                );
            }

            $userList.append($item);
        });
    }

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.type === "user_list") {
            renderUserList(data.users || []);
        } else {
            appendMessage(data.username, data.message);
        }
    };

    chatSocket.onclose = function () {
        appendMessage("system", "Connection closed");
    };

    function sendCurrentMessage() {
        const $input = $("#message-input");
        const message = $input.val().trim();
        if (!message) {
            return;
        }
        chatSocket.send(JSON.stringify({ message: message }));
        $input.val("");
    }

    $("#send-btn").on("click", function () {
        sendCurrentMessage();
    });

    $("#message-input").on("keypress", function (event) {
        if (event.which === 13) {
            sendCurrentMessage();
        }
    });
});