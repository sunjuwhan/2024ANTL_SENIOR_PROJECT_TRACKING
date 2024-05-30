from math import radians, sin, cos, sqrt

def get_distance(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (미터 단위)
    R = 6371000.0

    # 위도 및 경도를 라디안으로 변환
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # 두 지점 간의 차이를 계산
    delta_lon = lon2_rad - lon1_rad
    delta_lat = lat2_rad - lat1_rad

    # x축과 y축으로의 거리 계산
    x = R * delta_lon * cos((lat1_rad + lat2_rad) / 2)
    y = R * delta_lat

    return x, y

# 예시 좌표
lat1 = 37.7749
lon1 = -122.4194
lat2 = 34.0522
lon2 = -118.2437

x_distance, y_distance = get_distance(lat1, lon1, lat2, lon2)
print("x축으로 {:.2f} 미터, y축으로 {:.2f} 미터 이동해야 합니다.".format(x_distance, y_distance))
