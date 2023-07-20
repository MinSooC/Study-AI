import cv2

vcap = cv2.VideoCapture(0)

w = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # cam의 width 값
h = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # cam의 height 값
codec = cv2.VideoWriter_fourcc(*'DIVX')  # codec 형식 지정, *'FMP4' 로 지정하면 파일을 mp4로 저장 가능

fps = round(vcap.get(cv2.CAP_PROP_FPS))
delay = round(1000 / fps)

out = cv2.VideoWriter('out.avi', codec, fps, (w, h))

print(fps, delay)

while True:
    ret, frame = vcap.read()

    # 카메라 값을 제대로 잡지 못하면 ret 값은 False로 나온다.
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # 프레임 좌우반전, 0은 상하반전

    # inference 작업
    out.write(frame)
    cv2.imshow('cam', frame)

    if cv2.waitKey(1) == 27:
        break

out.release()
vcap.release()
cv2.destroyAllWindows()