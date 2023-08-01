import numpy as np
import mediapipe as mp
import time
import cv2

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
faceimg = cv2.imread('face_mk.png', cv2.IMREAD_UNCHANGED)
faceimg = cv2.resize(faceimg, (200, 200))

def face_overlay(background_img, img_to_overlay, x, y, overlay_size = None):
    try:
        # 들어오는 이미지가 매 순간 유동적이기에 그 순간을 copy 해야한다.
        bg = background_img.copy()  # 3채널
        ov = img_to_overlay.copy()  # 결과적으로 img_to_overlay도 copy를 했더니 끊기지 않고 더 부드러워졌다.

        if bg.shape[2] == 3:
            bg = cv2.cvtColor(bg, cv2.COLOR_BGR2BGRA)  # 3채널을 4채널로 변경 (알파 채널 추가)

        if overlay_size is not None:
            ov = cv2.resize(ov, overlay_size)

        b, g, r, a = cv2.split(ov)  # 마스크 이미지를 채널로 분리

        mask = cv2.medianBlur(a, 5)

        h, w, _ = ov.shape
        roi = bg[int(y - h/2):int(y + h/2), int(x - w/2):int(x + w/2)]  # 마스크가 위치해 있어야 할 영역 (이미지의 중심좌표 기준)

        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))  # 실제 부분에서 마스크가 제외된 부분
        img2_fg = cv2.bitwise_and(ov, ov, mask=mask)  # 실제 부분에서 마스크가 적용된 부분

        bg[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] = cv2.add(img1_bg, img2_fg)

        bg = cv2.cvtColor(bg, cv2.COLOR_BGRA2BGR)
        return bg

    except:
        return background_img


while True:
    ret, img = cap.read()

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # bgr 채널을 rgb 채널로 바꿈
    result = faceMesh.process(imgRGB)
    ih, iw, ic = img.shape

    if result.multi_face_landmarks:
        for faceLms in result.multi_face_landmarks:
            # 찍은 얼굴 사진의 포인트 좌표값 가져오기
            xy_point = []  # [[x, y]]
            for c, lm in enumerate(faceLms.landmark):
                xy_point.append([lm.x, lm.y])
                # img = cv2.circle(img, (int(lm.x * iw), int(lm.y * ih)), 1, (255, 0, 0), 1)

        top_left = np.min(xy_point, axis=0)
        bottom_right = np.max(xy_point, axis=0)
        mean_xy = np.mean(xy_point, axis=0)

        # img = cv2.circle(img, (int(mean_xy[0] * iw), int(mean_xy[1] * ih)), 4, (0, 0, 255), 2)  # 얼굴의 가운데 지점에 빨간색으로 표시

        face_width = int(bottom_right[0] * iw) - int(top_left[0] * iw)
        face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

        if face_width > 0 and face_height > 0:
            img = face_overlay(img, faceimg, int(mean_xy[0]*iw), int(mean_xy[1]*ih), (face_width + 150, face_height + 150))

    cv2.imshow('face', img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
