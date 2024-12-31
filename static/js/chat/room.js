console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersItemContainer = document.querySelector("#onlineUsersItemContainer");

function onlineUsersAdd(user) {
  // if (document.querySelector(`#${user}`)) return;
  let newdiv = document.createElement("div");
  newdiv.className = "online-user-item";
  newdiv.id = user;
  console.log(newdiv);
  newdiv.innerHTML = `
            <div class="user-status"></div>
            <span>${user}</span>
          `;
  onlineUsersItemContainer.appendChild(newdiv);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersRemove(user) {
  let oldOption = document.querySelector(`#${user}`);
  if (oldOption !== null) oldOption.remove();
}


// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
  if (e.keyCode === 13) {  // enter key
    chatMessageSend.click();
  }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function(e) {
  if (chatMessageInput.value.length === 0) return;
  // TODO: forward the message to the WebSocket
  var messageInput = document.querySelector("#id_message_send_input").value;
  var currentTime = new Date();
  var time = currentTime.toLocaleTimeString();
  chatSocket.send(JSON.stringify({
      message: messageInput,
      username: username,
      time: time
  }));
  chatMessageInput.value = "";
};


let chatSocket = null;

function connect() {
  chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

  chatSocket.onopen = function(e) {
    console.log("Successfully connected to the WebSocket.");
  }

  chatSocket.onclose = function(e) {
    console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
    setTimeout(function() {
      console.log("Reconnecting...");
      connect();
    }, 2000);
  };


  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    switch (data.type) {
      
      case "chat_message":
        var messageContainer = document.querySelector("#id_chat_item_container");
        var div = document.createElement("div");
        div.className = "chat-message";
        div.innerHTML = `<div class="message-content">
        <div class="message-text">${data.message}</div>
        <div class="message-timestamp">${data.time}</div>
        <div class="message-username">${data.username.charAt(0).toUpperCase() + data.username.slice(1)}</div>
        </div>`;
        document.querySelector("#chatMessageSend").value = "";
        messageContainer.appendChild(div);
        messageContainer.scrollTop = messageContainer.scrollHeight;
        break;
        
      case "user_join":
        let joinMessage = document.querySelector("#joinLeftMessage");       
        joinMessage.innerHTML = data.users[data.users.length - 1] + " joined the room.\n"; 
        onlineUsersItemContainer.innerHTML = ''; 
        data.users.forEach(user => {
          onlineUsersAdd(user);
        });
        console.log(data.users);
        break;
        
      case "user_leave":
        let LeftMessage = document.querySelector("#joinLeftMessage");
        LeftMessage.innerHTML = data.user + " left the room.\n";
        onlineUsersRemove(data.user);
        console.log(data.users);
        break;
        
      default:
        console.error("Unknown message type!");
        break;
    }
  };

  chatSocket.onerror = function(err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Closing the socket.");
    chatSocket.close();
  }
}
connect();


chatMessageSend.onclick = function() {
  if (chatMessageInput.value.length === 0) return;
  chatSocket.send(JSON.stringify({
    "message": chatMessageInput.value,
    username: JSON.parse(document.getElementById('username').textContent) ,
  }));

  $.ajax({url: window.location.href + 'save-message/',
    method: "POST",
    data: { content: chatMessageInput.value },
    error: function (error) {
      console.error("Error fetching project details: ", error);
    },
  });
  
  chatMessageInput.value = "";
};