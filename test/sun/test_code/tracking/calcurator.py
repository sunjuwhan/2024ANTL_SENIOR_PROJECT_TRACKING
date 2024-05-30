import math



degree_width=math.radians(60) #가로로 총 60도
degree_length=math.radians(60) #세로로 총 120도

width=640
lenght=480
height=1 # m


relative_length=2*(math.tan(degree_width/2))*height #실제 세로로 퍼져있는거리
relative_width=2*(math.tan(degree_width/2))*height #실제로 가로로 퍼져있는거리



def cal_distance(x_pos,y_pos):
    x=((x_pos-(width/2))/width)*relative_width
    y=((y_pos-(lenght/2))/lenght)*relative_length
    return (x,y)


print("{:>20}{:>12}{:>12}{:>12}".format("Class","Images","P","R"))