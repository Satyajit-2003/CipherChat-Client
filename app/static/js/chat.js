document.addEventListener('DOMContentLoaded', (event) => {
    get_users();
    console.log(username);
    const socket = io.connect("http://" + document.location.hostname + ":" + location.port);

    socket.on('connect', () => {
        console.log('Successfully connected to the socket...');
    });

    socket.on('message', (data) => {
        console.log('Received message:', data);
        console.log('Username:', username);
        if (data.from === username) {
            let strTime = timestamp_convert(data.timestamp);
            addMessage(data.message, strTime, 'received');
        }
    });
    
    function sending_func() {
        var message = messageInput.value;
        if (message === '') {
            return;
        }
        messageInput.value = '';
        socket.emit('message', { message: message, username: username});
        addMessage(message, timestamp_convert(Math.floor(Date.now()/1000)), 'sent');
    }

    if (username !== '') {
        console.log(username);
        console.log('Chat screen is present');
        document.getElementById('sendButton').addEventListener('click', function() {
            sending_func();
        });

        document.getElementById('messageInput').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                sending_func();
            }
        });
        populate_chat(username);
    }   

});

function populate_chat(user) {
    fetch('/get_messages?user=' + user)
        .then(response => response.json())
        .then(data => {
            data.messages.forEach(message => {
                addMessage(message.message, timestamp_convert(message.timestamp), message.send === true ? 'sent' : 'received');
            });
        });
}

function addMessage(message, time, type) {
    var messageElement = document.createElement('div');
    if (type === 'sent') {
        messageElement.classList.add('message', 'sent');
        var receivedDiv = document.createElement('div');
        receivedDiv.classList.add('sent');
    } else {
        messageElement.classList.add('message', 'received');
        var receivedDiv = document.createElement('div');
        receivedDiv.classList.add('received');
    }


    var messageContent = document.createElement('p');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;
    receivedDiv.appendChild(messageContent);

    var timestamp = document.createElement('span');
    timestamp.classList.add('timestamp');
    timestamp.textContent = time;
    receivedDiv.appendChild(timestamp);

    messageElement.appendChild(receivedDiv);
    for (let i = 0; i < 2; i++) {
        const br = document.createElement('br');
        document.querySelector('.messages').appendChild(br);
    }
    
    document.querySelector('.messages').appendChild(messageElement);
    
    messageElement.scrollIntoView();
}

function timestamp_convert(timestamp) {
    let date = new Date(timestamp * 1000);
    let hours = date.getHours();
    let minutes = "0" + date.getMinutes();
    return hours + ':' + minutes.substr(-2);
}

function get_users() {
    fetch('/get_users')
    .then(response => response.text())
    .then(data => {
        console.log('Raw response from /get_users:', data);
        let users = JSON.parse(data);
        let userListDiv = document.querySelector('.user-list');

        users.forEach(user => {
            
            let aTag = document.createElement('a');
            aTag.href = '/home?user=' + user.user;
            let userDiv = document.createElement('div');
            userDiv.classList.add('user');

            aTag.appendChild(userDiv);

            let username = document.createElement('h5');
            username.classList.add('username');
            username.textContent = user.user.charAt(0).toUpperCase() + user.user.slice(1);
            userDiv.appendChild(username);

            let status = document.createElement('p');
            status.classList.add('status');
            status.textContent = user.status ? 'Online' : 'Offline';
            userDiv.appendChild(status);

            userListDiv.appendChild(aTag);
        });
    });
}

