username = localStorage.getItem("username");
group_name = localStorage.getItem("group_name");

color_json = {};

function make_connection() {
    const chatSocket = new WebSocket(
        'ws://' +
        window.location.host +
        '/ws/groupchat/' + username + '/to/' + group_name + '/'
    );

    chatSocket.onmessage = function(e) {
        data = JSON.parse(e.data);

        div_group_message_main = document.createElement("div");
        div_group_message_main.classList.add("d-flex");
        div_group_message_main.classList.add("flex-row");
        div_group_message_main.classList.add("pl-3");
        div_group_message_main.classList.add("pr-3");
        div_group_message_main.classList.add("pb-1");
        div_group_message_main.setAttribute("data-who", data.sender);

        last_child = document.getElementById("chat").lastElementChild;

        b = false;
        if (last_child == null) {
            div_group_message_main.classList.add("pt-3");
            img = document.createElement("img");
            img.src = "data:image/png;base64,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";
            img.height = "30";
            img.width = "30";
            div_group_message_main.appendChild(img);
        } else {
            if (last_child.dataset.who != data.sender) {
                div_group_message_main.classList.add("pt-3");
                img = document.createElement("img");
                img.src = "data:image/png;base64,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";
                img.height = "30";
                img.width = "30";
                div_group_message_main.appendChild(img);
            } else {
                b = true;
            }
        }

        div_chat = document.createElement("div");
        div_chat.classList.add("chat");
        div_chat.classList.add("pb-3");
        div_chat.classList.add("pl-3");
        div_chat.classList.add("pr-3");
        div_chat.classList.add("ml-2");

        if (b) {
            div_group_message_main.style.marginLeft += "30px";
        }

        if (color_json[data.sender] == undefined) {
            randomColor = getRandomColor();
            color_json[data.sender] = randomColor;
        } else {
            randomColor = color_json[data.sender];
        }

        if (last_child == null) {
            div_chat.classList.add("pt-1");
            name_p = document.createElement("p");
            name_p.style.color = randomColor;
            name_p.innerText = data.sender;
            div_chat.appendChild(name_p);
        } else {
            if (last_child.dataset.who != data.sender) {
                div_chat.classList.add("pt-1");
                name_p = document.createElement("p");
                name_p.style.color = randomColor;
                name_p.innerText = data.sender;
                div_chat.appendChild(name_p);
            } else {
                div_chat.classList.add("pt-3");
            }
        }
        span_message_person = document.createElement("span");
        span_message_person.innerText = data.message;
        div_chat.appendChild(span_message_person);
        div_group_message_main.appendChild(div_chat);

        document.getElementById("chat").appendChild(div_group_message_main);
    };

    chatSocket.onclose = function(e) {
        console.error(e);
    };

    var input = document.getElementById("input");
    var send = document.getElementById("send");
    send.addEventListener("click", function(event) {
        if (input.value == "") {
            return;
        }
        chatSocket.send(JSON.stringify({
            'message': input.value,
            'sender': username
        }));
        div_person = document.createElement("div");
        div_person.classList.add("d-flex");
        div_person.classList.add("flex-row");
        div_person.classList.add("pr-3");
        div_person.classList.add("justify-content-end");
        div_person.classList.add("pl-3");
        div_person.classList.add("pb-1");
        div_person.setAttribute("data-who", "me");

        div_message = document.createElement("div");
        div_message.classList.add("bg-white");
        div_message.classList.add("mr-2");
        div_message.classList.add("p-3");

        span_message = document.createElement("span");
        span_message.classList.add("text-muted");
        span_message.innerText = input.value;

        div_message.appendChild(span_message);
        div_person.appendChild(div_message);

        b = false;

        last_child = document.getElementById("chat").lastElementChild;
        if (last_child == null) {
            div_person.classList.add("pt-3");
            img = document.createElement("img");
            img.src = "data:image/png;base64,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";
            img.width = "30";
            img.height = "30";
            div_person.appendChild(img);
        } else {
            if (last_child.dataset.who != "me") {
                div_person.classList.add("pt-3");
                img = document.createElement("img");
                img.src = "data:image/png;base64,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";
                img.width = "30";
                img.height = "30";
                div_person.appendChild(img);
            } else {
                b = true;
            }
        }

        if (b) {
            div_person.style.marginRight += "30px";
        }

        document.getElementById("chat").appendChild(div_person);

        input.value = "";
    });

    // document.querySelector('#echo-message-submit').onclick = function(e) {
    //     const messageInputDom = document.querySelector('#echo-message-input');
    //     const message = messageInputDom.value;
    //     echoSocket.send(JSON.stringify({
    //         'message': message
    //     }));
    //     messageInputDom.value = '';
    // };
}

make_connection();

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}