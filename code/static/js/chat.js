// 'use strict';
// ngrok를 사용할 때 document.domain 및 location.port 속성은 로컬 개발 서버의 속성과 다르지만 
// 그에 따라 연결 URL을 업데이트하는 한 코드는 여전히 작동해야 합니다.
const socket = io.connect('http://' + document.domain + ':' + location.port); //'http://localhost:8000'
                                    // localhost                8000
// var socket = io.connect("http://2598-221-150-54-199.ngrok-free.app");
const saveButton = document.querySelector("#save-button"); // 채팅 내용 저장
const nickname = document.querySelector("#nickname");
const chatList =document.querySelector(".chatting-list");
const chatInput = document.querySelector(".chatting-input");
const sendButton = document.querySelector(".send-button");
const displayContainer = document.querySelector(".display-container");
// 채팅 내용 저장
saveButton.addEventListener("click", saveChatHistory);
//
function saveChatHistory() {
    const chatItems = chatList.getElementsByTagName('li');
    let chatHistory = "";
    for (let i = 0; i < chatItems.length; i++) {
        const item = chatItems[i];
        // const name = item.querySelector('.user').textContent;
        const message = item.querySelector('.message').textContent;
    //     const time = item.querySelector('.time').textContent;
    //     chatHistory += `${name} (${time}): ${message}\n`;
        chatHistory += `${message}\n`;
    }
    const file = new Blob([chatHistory], {type: 'text/plain'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(file);
    a.download = 'chat_history.txt';
    a.click();
}// txt로 채팅 내용 저장
//keypress -> keyup 
chatInput.addEventListener('keyup', (e) => {
    // if (e.keyCode === 13) {
    if (e.key === 'Enter') {
        send();
    }
});

function send(){
    const param = {
        name: nickname.value,   // input이라서 value 접근 가능.
        msg : chatInput.value,
    };
    socket.emit("chatting", param);
    chatInput.value = ""; // Clear the input field after the message is sent
}

sendButton.addEventListener("click",send)

// 받아 줄 때는 socket.on 사용.
socket.on("chatting", (data)=>{
    console.log(data)
    const {name, msg, time} = data;
    const item = new LiModel(name, msg, time);
    item.makeLi()

    // 스크롤 밑으로
    displayContainer.scrollTo(0, displayContainer.scrollHeight)
})

function LiModel(name, msg, time){
    this.name = name;
    this.msg = msg;
    this.time = time;

    this.makeLi = ()=>{
        const li = document.createElement("li");
        li.classList.add(nickname.value === this.name ? "sent" : "received")
        const dom = ` <span class="profile">
        <span class="user">${this.name}</span>
        <img  class="image" src="../static/img/Unknown.png" alt="any">
        </span>
        <span class="message">${this.msg}</span>
        <span class="time">${this.time}</span>`; 
        //img sent received 조절.  //위치가 html 기준이네......// http://placeimg.com/50/50/any -> 랜덤 이미지
    li.innerHTML = dom;
    chatList.appendChild(li);
    };
}

// 정상적으로 불러와졌는지 확인
console.log(socket);