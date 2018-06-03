let chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + roomName + '/');

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let message = data['message'];

    console.log('message received: ' + data);

    let newDiv = document.createElement('div');
    newDiv.setAttribute('class', 'one_message');
    newDiv.innerHTML += '<p>' + '</p>';
    newDiv.innerHTML = '<p>' + message + '</p>';

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