[<img width="1333" alt="갈 이미지" src="https://user-images.githubusercontent.com/103846429/236394181-ecc6f108-b4f4-41cf-8ec4-7f99862906be.png">](https://www.notion.so/modulabs/70d9271884ab4c3d909b617a999e5adc)  
# :dog: 갈! [<<암묵적 언어폭력 탐지에 관한 연구>>](https://m05.notion.site/20d81a929b294eb4a28a248c9acfe28b?pvs=4)  
:telescope: 본 프로젝트는 “아이펠”과정 중 “아이펠톤”기간에 진행하였습니다.  
:calendar: `(23.03.24 ~ 23.05.08)`  

---

:microscope: 프로젝트 소개
-----
:newspaper: 현 사회의 언어적 비윤리 문제를 최소화하고자 본 프로젝트를 진행하게 되었습니다.  

비윤리적 언어폭력은 명시적[암묵적]인 대화를 통해 전달이 되기에  
딥러닝 모델을 통해 해당 대화의 의도를 파악하고 예측을 하려고 합니다.  

---
:pushpin: sample 1 

<img width="594" alt="카톡 샘플" src="https://user-images.githubusercontent.com/103846429/236128188-35e38b52-4eaa-499e-96cc-5da2b946a3ca.png">

:pushpin: sample 2
>태경씨 오늘 퇴근 일찍하네?  
아.. 저 바쁜 일이 있어서요.  
난 오늘 야근하는 거 안보여? 요새 신입은 사회생활 참 모르네?  
팀장님 저 해야할 일은 다 마쳤는데요  
지금 내가 여기 앉아있는데 일찍 간다는 게 말이돼? 일 더 줄까?  
>아닙니다. 죄송합니다.  

|class|명시적인 언어폭력|암묵적인 갈취 대화|암묵적인 기타 괴롭힘 대화|일상적인 대화문|암묵적인 직장 내 괴롭힘 대화|암묵적인 협박 대화|
|----|----|----|----|----|----|----|  

위의 이미지[텍스트]형태의 대화문을 모델에 넣었을 때 `6개의 class 중에 1가지` 로 분류를 목표로 합니다.  

---
:computer: 웹 서비스
---
<img width="1336" alt="웹 이미지" src="https://user-images.githubusercontent.com/103846429/236398564-c68f75dc-1a7d-4e17-83a3-12e73f4da815.png">

---
:cd: 데이터셋
---
<img width="497" alt="데이터셋" src="https://user-images.githubusercontent.com/103846429/236128663-313077b5-e3bd-4c48-b8ac-0e15bd10f73c.png">

---
:chart_with_upwards_trend: 사용한 모델
---
<img width="1500" alt="BERT model" src="https://user-images.githubusercontent.com/103846429/236450943-f28a9589-2df2-4315-9596-2867afccb2be.png">


---
:dizzy: 접근 방식
---
<img width="1500" alt="OOD" src="https://user-images.githubusercontent.com/103846429/236450979-57e38c10-13c4-45f8-a26f-09524a68e766.png">

