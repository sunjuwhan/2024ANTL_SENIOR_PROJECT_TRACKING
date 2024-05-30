import cv2

# 카메라 객체 생성
cap = cv2.VideoCapture(0)  # 0번 카메라를 사용 (일반적으로 라즈베리파이에서는 0번 카메라가 연결된 카메라)

while True:
    # 카메라에서 프레임 읽기
    ret, frame = cap.read()
    print(type(frame))
    print(len(frame))
    
    # 프레임 읽기에 성공하면 화면에 표시
    if ret:
        cv2.imshow('Camera', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 카메라 객체 해제
cap.release()
# 모든 창 닫기
cv2.destroyAllWindows()
