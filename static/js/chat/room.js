console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersContainer = document.querySelector("#id_onlineUsers_item_container");


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
        break;
        
      default:
        console.error("Unknown message type!");
        break;
      }
        
    // Scroll to the bottom of the chat container
    messageContainer.scrollTop = messageContainer.scrollHeight;
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
  chatMessageInput.value = "";
};  