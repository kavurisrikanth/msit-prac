let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
let chatSocket = new WebSocket(
    ws_scheme + '://' + window.location.host +
    '/ws/chat/' + roomName + '/');

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data),
        message = data['message'];
    let sender = data['sender'],
        firstName = data['first_name'],
        lastName = data['last_name'],
        timestamp = JSON.parse(data['timestamp']);

    let newDiv = document.createElement('div');

    newDiv.setAttribute('class', 'one_message');
    newDiv.setAttribute('class', (sender === currentUsername) ? 'sent': 'received');
    newDiv.innerHTML += '<p class="sender_name">' + firstName + ' ' + lastName + ' ' + timestamp + '</p>';
    newDiv.innerHTML += '<hr>';
    newDiv.innerHTML += '<p class="msg_text">' + message + '</p>';

    document.querySelector('#chat-history').appendChild(newDiv);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    let messageInputDom = document.querySelector('#chat-message-input'),
        message = messageInputDom.value,
        roomLabel = document.querySelector('#current_room_label').getAttribute('value'),
        sender = document.querySelector('#sender').getAttribute('value');

    chatSocket.send(JSON.stringify({
        'message': message,
        'room_label': roomLabel,
        'sender': sender
    }));

    messageInputDom.value = '';
};