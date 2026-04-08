// static/js/chat.js

function addMessage(text, type) {
    let msg = document.createElement("div");
    msg.className = "message " + type;
    msg.innerHTML = text;

    document.getElementById("chatBody").appendChild(msg);
    msg.scrollIntoView();

    return msg;
}

function sendMessage() {
    let input = document.getElementById("input");
    let text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    let typing = addMessage(
        '<span class="typing"><span>.</span><span>.</span><span>.</span></span>',
        "bot"
    );

    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        typing.remove();
        addMessage(data.reply, "bot");
    });
}