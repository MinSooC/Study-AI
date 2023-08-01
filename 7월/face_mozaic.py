import cv2
import mediapipe as mp
import time
import numpy as np

# 캠에서 화면을 캡처해서 가져오기
cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()

while True:
    sucess, img = cap.read()

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # bgr 채널을 rgb 채널로 바꿈
    result = faceMesh.process(imgRGB)

    if result.multi_face_landmarks:
        for faceLms in result.multi_face_landmarks:
            # 찍은 얼굴 사진의 포인트 좌표값 가져오기
            xy_point = []  # [[x, y]]
            for c, lm in enumerate(faceLms.landmark):
                xy_point.append([lm.x, lm.y])

        top_left = np.min(xy_point, axis = 0)  # 좌상단 끝점
        bottom_right = np.max(xy_point, axis = 0)  # 우하단 끝점
        mean_xy = np.mean(xy_point, axis = 0)  # 사진 정중앙
    
    ih, iw, ic = img.shape  # 전체 사진의 높이, 길이, 채널 구하기

    face_width = int(bottom_right[0] * iw) - int(top_left[0] * iw)
    face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

    # 시작 포인트 구하기
    sx = int(top_left[0] * iw)
    sy = int(top_left[1] * ih)
    roi = img[sy:sy+face_height, sx:sx+face_width]  # 시작포인트부터, 찾은 얼굴의 높이만큼을 잘라와라

    # 모자이크 처리 : 얼마나 축소하느냐에 따라서 간격이 달라진다.
    roi = cv2.resize(roi, (int(face_width / 20), int(face_height / 20)))
    roi = cv2.resize(roi, (face_width, face_height), interpolation = cv2.INTER_AREA)

    # 원래 출력할 이미지에 갖다 붙이기
    try:
        img[sy:sy+face_height, sx:sx+face_width] = roi
    except:
        pass

    cv2.imshow('face', img)

    if cv2.waitKey(1) == ord('q'):
        break
