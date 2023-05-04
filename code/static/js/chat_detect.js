//
const socket = io.connect('http://' + document.domain + ':' + location.port + '/detect'); //'http://localhost:8000'
const dropbox = document.querySelector('.file_box');
const input_filename = document.querySelector('.file_name');
const output_detect = document.querySelector('.text_detect');
let target = document.querySelector("#dynamic"); // dynamic
let fileDropped = false; // 파일 드랍 되기전에는 false
// sentence 설정.
function splitSentence() {
    let sentence = "img & txt파일 드롭 해보거라 喝!".split("");
    return sentence;
}
// 타이핑 리셋
function resetTyping() {
    target.textContent = "";
    dynamic(splitSentence());
}
// 한글자씩 sentence 출력
function dynamic(sentence) {
    //variable is false or not true, then you would use !. 
    //variable is true, then you wouldn't use !.
    if (!fileDropped) {  // fileDropped = false 일때만 실행
        console.log(sentence);
        if (sentence.length > 0) {
            target.textContent += sentence.shift();
            setTimeout(function () {
                dynamic(sentence);
            }, 80); // call dynamic every 0.08 seconds
        } else {
            setTimeout(resetTyping, 3000) // Called after 3 seconds
        }
    }
}
// https://stickode.tistory.com/529
//박스 안에 drag 하고 있을 때
dropbox.addEventListener('dragover', function (e) {
    e.preventDefault();
    this.style.backgroundColor = 'rgb(13 110 253 / 25%)';
});

//박스 밖으로 drag가 나갈 때
dropbox.addEventListener('dragleave', function (e) {
    this.style.backgroundColor = 'white';
});

// const CLASS_LABEL = ["갈취", "기타 괴롭힘", "직장 내 괴롭힘", "협박", "일상 대화", "암묵적 언어 폭행"];

// when dropped in the box
dropbox.addEventListener('drop', function (e) {
    e.preventDefault();
    this.style.backgroundColor = 'white';
    fileDropped = true; // 드롭 되었을 때 dynamic(sentence) 실행 안됨

    // read the contents of the dropped file
    let file = e.dataTransfer.files[0];
    let fileType = file.type;

    // check if the dropped file is an image
    if (fileType.indexOf("image") != -1) {
        // create a new image element and set its source to the dropped file
        let img = document.createElement("img");

        img.onload = function () {
            // Resize image to fit the file_box div
            if (img.width > img.height) {
                img.style.width = "100%";
                img.style.height = "75%";
            } else {
                img.style.width = "75%";
                img.style.height = "100%";
            }
            // Convert the image to a data URL
            let canvas = document.createElement("canvas");
            // Create a new canvas to hold the resized image
            let canvas_resized = document.createElement("canvas");
            let width = img.width;
            let height = img.height;
            // Check if the image needs to be resized
            if (width > 800 || height > 600) {
                // Resize the image to fit within 800 x 600 dimensions
                if (width / height > 800 / 600) {
                    width = 800;
                    height = Math.round(height * (800 / img.width));
                } else {
                    width = Math.round(width * (600 / img.height));
                    height = 600;
                }
            }
            canvas_resized.width = width;
            canvas_resized.height = height;
            let ctx_resized = canvas_resized.getContext("2d");
            ctx_resized.drawImage(img, 0, 0, width, height);
            let fileIamge = canvas_resized.toDataURL(fileType);
            // flask로 보내기
            socket.emit("image data", fileIamge, "kakao_img.png");
        };

        img.src = URL.createObjectURL(file);
        console.log(img.src)
        // 이미지 웹상에서 출력
        dropbox.innerHTML = "";
        dropbox.appendChild(img);
        // flask에서 받기
        socket.on("result", function (result) {
            output_detect.innerHTML = result;
            // console.log(result);
        });
    } else {
        // read the contents of the dropped file as text
        let reader = new FileReader();
        reader.readAsText(file);
        // set the contents of the file as the text of the input element
        reader.onload = function () {
            let fileText = reader.result;
            dropbox.innerHTML = fileText;
            // flask로 보내기
            socket.emit('text data', fileText)
            console.log(fileText);
            // flask에서 받기
            socket.on("result", function (result) {
                output_detect.innerHTML = result;
                // console.log(result);
            });
        };
    }
});
// before dropping 드랍 전에만 실행
dynamic(splitSentence());