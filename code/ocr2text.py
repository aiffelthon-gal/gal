# 참고한 링크: https://yunwoong.tistory.com/148

# 라이브러리 불러오기
import os, io, cv2, platform, json, requests # cv2 4.5.3
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image # 8.3.2
from google.cloud import vision
from google.cloud import vision_v1
from google.oauth2 import service_account

# main # putText # filter_boxes # sort_texts # remove_newlines
def main(img_path, e=1, y_tolerance=3, y_large_tolerance=90):
    
    with open(img_path, 'rb') as image_file:
        content = image_file.read()

    # 이미지 바이트 스트림으로 변환
    image = vision_v1.Image(content=content) # content=content

    # Google Cloud Vision API에 연결하기 위해 인증 정보를 가져옴
    credentials = service_account.Credentials.from_service_account_file('')

    # Google Cloud Vision API와 연결
    client = vision_v1.ImageAnnotatorClient(credentials=credentials)

    # 이미지에서 텍스트 감지하기
    response = client.text_detection(image=image)
    texts = response.text_annotations[1:]

    img = cv2.imread(img_path)
    roi_img = img.copy()

    # 바운딩 박스의 세로 길이가 가장 많이 나오는 길이보다 작은 텍스트들 제외하기
    texts = filter_boxes(texts, e) # filter_boxes -> filtered_texts

    # 결과 출력
    sorted_text = sort_texts(texts, y_tolerance) # sort_texts -> result



    sorted_text = remove_newlines(sorted_text, y_large_tolerance) # remove_newlines -> sort_texts

    conversation = ''

    for text in sorted_text:

        if text == '\n':
            conversation = conversation.strip()
            conversation += '\n'

        else:
            conversation += text.description + ' '

            vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices])

            ocr_text = text.description
            x1 = text.bounding_poly.vertices[0].x
            y1 = text.bounding_poly.vertices[0].y
            x2 = text.bounding_poly.vertices[1].x
            y2 = text.bounding_poly.vertices[2].y

#             cv2.rectangle(roi_img, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0), 2) 
            roi_img = putText(roi_img, ocr_text, x1, y1 - 30, font_size=30) # putText -> opencv_image

    conversation = conversation.strip()

    return conversation

#     print(conversation) ##############################
#     plt_imshow(["Original", "ROI"], [img, roi_img], figsize=(16, 10)) ###########################

def putText(image, text, x, y, color=(0,0,255), font_size=22):
    if type(image) == np.ndarray:
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(color_coverted)

    if platform.system() == 'Darwin':
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows':
        font = 'malgun.ttf'
    else:
        font = 'NanumGothic.ttf'
        
    image_font = ImageFont.truetype(font, font_size)
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)

    draw.text((x, y), text, font=image_font, fill=color)
    
    numpy_image = np.array(image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    return opencv_image

# def plt_imshow(title='image', img=None, figsize=(8 ,5)):
#     plt.figure(figsize=figsize)

#     if type(img) == list:
#         if type(title) == list:
#             titles = title
#         else:
#             titles = []
 
#             for i in range(len(img)):
#                 titles.append(title)
 
#         for i in range(len(img)):
#             if len(img[i].shape) <= 2:
#                 rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
#             else:
#                 rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
 
#             plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
#             plt.title(titles[i])
#             plt.xticks([]), plt.yticks([])
 
#         plt.show()
    
#     else:
#         if len(img.shape) < 3:
#             rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
#         else:
#             rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
#         plt.imshow(rgbImg)
#         plt.title(title)
#         plt.xticks([]), plt.yticks([])
#         plt.show()

def filter_boxes(texts, e=5):
    # 바운딩 박스의 세로 길이를 구함
    height_dict = {}
    for text in texts:
        vertices = text.bounding_poly.vertices
        height = abs(vertices[3].y - vertices[0].y)
        if height not in height_dict:
            height_dict[height] = 0
        height_dict[height] += 1
    most_common_height = max(height_dict, key=height_dict.get)
    
    # 가장 많이 나온 세로 길이와 다른 바운딩 박스를 필터링
    filtered_texts = []
    for text in texts:
        vertices = text.bounding_poly.vertices
        height = abs(vertices[3].y - vertices[0].y)
        if most_common_height-e <= height and height <= most_common_height+e:
            filtered_texts.append(text)
    
    return filtered_texts

def sort_texts(texts, y_tolerance=10):
    # y축을 기준으로 먼저 정렬
    sorted_texts = sorted(texts, key=lambda x: x.bounding_poly.vertices[0].y)
    result = []
    current_row = []
    previous_y = None
    
    for text in sorted_texts:
        if text == '\n':
            continue
        y = text.bounding_poly.vertices[0].y
        
        if previous_y is None:
            # 첫번째 요소
            current_row.append(text)
        elif abs(y - previous_y) <= y_tolerance:
            # 같은 줄에 속하는 경우
            current_row.append(text)
        else:
            # 다른 줄에 속하는 경우
            current_row.sort(key=lambda x: x.bounding_poly.vertices[0].x)
            result.extend(current_row)
            result.append('\n')
            current_row = [text]
        
        previous_y = y
    
    if len(current_row) > 0:
        current_row.sort(key=lambda x: x.bounding_poly.vertices[0].x)
        result.extend(current_row)
    
    return result

def remove_newlines(sorted_texts, y_large_tolerance=90):
    i = 1
    while i < len(sorted_texts) - 1:
        
        if sorted_texts[i] == '\n':
            y_top = sorted_texts[i-1].bounding_poly.vertices[0].y
            y_bottom = sorted_texts[i+1].bounding_poly.vertices[2].y
            
            if abs(y_bottom - y_top) <= y_large_tolerance:
                del sorted_texts[i]
                continue
        i += 1
        
    return sorted_texts

