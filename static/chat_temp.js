function sendMessage(){
    let input = document.getElementById("input");
    let input_text = input.value.trim()
    if (!input_text){return};

    addMessage(input_text,"user");
    input.value = "";

    let typing = addMessage(
        '<span class="typing"><span>.</span><span>.</span><span>.</span></span>',
        "bot"
    );
    fetch('http://127.0.0.1:5000/get',
        {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({message: input_text})
        }
    )
    .then(res=> res.json())
    .then(data=> {
        typing.remove();
        addMessage(data.response,"bot");
    })
    

}

function addMessage(text,type){
    let msg = document.createElement("div");
    msg.className = "message " + type;
    msg.innerHTML = text;

    document.getElementById("chatBody").appendChild(msg);
    msg.scrollIntoView();
    return msg;
}