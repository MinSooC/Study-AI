import cv2

vcap = cv2.VideoCapture(0)  # 기본 카메라 열기
fps = round(vcap.get(cv2.CAP_PROP_FPS))  # FPS 값을 받음
delay = round(1000 / fps)  # 딜레이가 있는지 유무 확인

print(fps, delay)

while True:
    ret, frame = vcap.read()

    if not ret:
        break
    
    # inference 작업
    
    cv2.imshow('cam', frame)

    if cv2.waitKey(1) == 27:
        break

vcap.release()
cv2.destroyAllWindows()
