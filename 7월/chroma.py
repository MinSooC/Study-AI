import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0)

back_frame = cv2.imread('images/starry_night.jpg')
back_frame = cv2.resize(back_frame,
                        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                         int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                        )
# 합성 변수
do_composit = False

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if do_composit:
        mask = cv2.inRange(frame, (0, 100, 0), (128, 255, 128))  # 내가 제거할 부분의 색상값 받아오기
        cv2.copyTo(back_frame, mask, frame)

    cv2.imshow('chroma', frame)

    if cv2.waitKey(1) == ord(' '):
        do_composit = not do_composit  # 스페이스 키를 누르면 do_composit 값이 바뀜
    elif cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
