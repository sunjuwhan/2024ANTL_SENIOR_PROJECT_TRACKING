from datetime import datetime

# 현재 날짜와 시간 가져오기
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y:%m:%d %H:%M')
print(formatted_datetime)