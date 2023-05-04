# -*- coding: utf-8 -*-
import base64
import os
import urllib
from datetime import datetime

import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# 두목대표님들 코드
import ocr2text
import text2cls

#
app = Flask(__name__)
app.config["SECRET_KEY"] = "all_rights"
socketio = SocketIO(app)  # from flask_socketio import SocketIO


#
@app.route("/index")
@app.route("/", methods=["GET", "POST"])
def index_page():
    return render_template("index.html")


#
@app.route("/detect", methods=["GET", "POST"])
def detect_page():
    # if request.method == 'GET':
    result = "분류 결과는 ??? 입니다."
    return render_template("detect.html", result=result)


#
@socketio.on("chatting")  # from flask_socketio import SocketIO
def handle_chatting(data):
    name = data["name"]
    msg = data["msg"]
    time = datetime.now().strftime("%I:%M %p")
    emit("chatting", {"name": name, "msg": msg, "time": time}, broadcast=True)


# Classification
# CLASS_DICT = {
#     0: "명시적인 언어폭력",
#     1: "일상적인 대화문",
#     2: "암묵적인 갈취 대화",
#     3: "암묵적인 기타 괴롭힘 대화",
#     4: "암묵적인 직장 내 괴롭힘 대화",
#     5: "암묵적인 협박 대화",
# }


# image 받기
# @socketio.on('image_url', namespace="/detect")
@socketio.on("image data", namespace="/detect")
def classification_image(img_data, fileName):  # fileIamge, "kakao_img.png"

    img_bytes = base64.b64decode(img_data.split(",")[1])
    # print(img_bytes)
    dir_path = "static/img/"
    # 이미지 다운로드 (img 폴더 안으로)
    with open(os.path.join(dir_path, fileName), "wb") as f:
        f.write(img_bytes)
######## 지영두목님 코드#############################################
    img_path = "static/img/kakao_img.png" 
    text = ocr2text.main(img_path, e=1.85, y_tolerance=3, y_large_tolerance=70)
    print("---------- 이미지에서 추출된 text ----------")
    print(text)
    result = text2cls.web_detect_1_2(text)
    print("---------- 해당 이미지의 text의 결과는 ----------")
    print(result)
##################################################################        img_path = "static/img/kakao_img.png"
    text = ocr2text.main(img_path, e=3, y_tolerance=3, y_large_tolerance=90)
    print("----------------text")
    print(text)
    result = text2cls.web_detect_1_2(text)
    print("-----------------------------프린트")
    print(result)
    emit("result", result)


# text 받기
@socketio.on("text data", namespace="/detect")
def classification_text(fileText):
######## 수경선생님 코드##############################################
    print("---------- txt파일 내의 text ----------")
    print(fileText)
    # result = text2cls.web_detect_1_3(fileText)
    result = text2cls.web_detect_1_2(fileText)
    print("---------- text의 결과는 ----------")
    print(result)
##################################################################
    emit("result", result)  # chat_detect로 보내기


# 실행
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=port)
    # socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

# http://127.0.0.1:8080
# 로컬 시스템에서만 액세스할 수 있는 루프백 주소
# http://192.168.0.102:8080
# 로컬 네트워크에서 장치를 식별하는 사설 IP 주소라는 것