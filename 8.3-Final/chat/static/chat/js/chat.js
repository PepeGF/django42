$(function () {
    const roomName = window.CHAT_CONFIG.roomName;
    const wsScheme = window.CHAT_CONFIG.wsScheme;

    const chatSocket = new WebSocket(
    wsScheme + "://" + window.location.host + "/ws/chat/" + encodeURIComponent(roomName) + "/"
);

    function appendMessage(username, message) {
        $("#messages-container").append(
            $("<p></p>").text(username + ": " + message)
        );
    }

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        appendMessage(data.username, data.message);
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