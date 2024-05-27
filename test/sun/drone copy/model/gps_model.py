from math import radians, sin, cos, sqrt, atan2
class GpsModel:
    def __init__(self) -> None:
        self.__latitude_deg=0.0 #위도
        self.__longitude_deg=0.0#경도
        self.__absolute_altitude=0.0
        self.__relative_altitude=0.0#실제 높이 
        self.__start_latitude=0.0
        self.__start_longitude=0.0
        
    def set_gps(self,latitude,longitude,absolute,relative):
        self.__latitude_deg=latitude
        self.__longitude_deg=longitude
        self.__absolute_altitude=absolute
        self.__relative_altitude=relative
    def set_start_gps(self,latitude,longitude):
        self.__start_latitude=latitude
        self.__start_longitude=longitude
    def get_start_gps(self):
        return self.__start_latitude,self.__start_longitude
    def get_gps(self):
        return(self.__latitude_deg,self.__longitude_deg,self.__absolute_altitude,self.__relative_altitude)
    
    def get_direction(self,lat1, lon1, lat2, lon2):
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