import gpiod

# gpiod 라이브러리를 사용하여 GPIO 컨트롤러 초기화
chip = gpiod.Chip('gpiochip4')

# 사용할 GPIO 핀 설정 (여기서는 GPIO 27을 사용합니다)
line = chip.get_line(27)

# 입력으로 설정 (스위치가 연결된 경우)
line.request(consumer="switch", type=gpiod.LINE_REQ_DIR_IN)

try:
    while True:
        # 스위치 값을 읽기
        value = line.get_value()

        # 스위치 값 출력
        print("스위치 값:", value)

except KeyboardInterrupt:
    # Ctrl+C를 눌러 프로그램을 종료할 때 GPIO 리소스 정리
    line.release()
    chip.close()