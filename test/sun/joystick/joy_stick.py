import spidev
import time
import os
import socket
import numpy
import cv2
from threading import *

import socket
HOST='192.168.50.63'  #내가 쏴야하는 곳 
PORT = 8080

def set_spi(num):
  spi=spidev.SpiDev()
  spi.open(num,0)
  spi.max_speed_hz=1000000   
  return spi


def ReadChannel(channel,spi):           
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def stabil_vrx(vrx_pos):
  if(vrx_pos>=500 and vrx_pos<=510):
    vrx_pos=500
  elif(vrx_pos>=0 and vrx_pos < 3):
    vrx_pos=0
  elif(vrx_pos>=1000 and vrx_pos <=1030):
    vrx_pos=1000
  return vrx_pos

def stabil_vry(vry_pos):
  if(vry_pos>=495 and vry_pos<=510):
    vry_pos=500
  elif(vry_pos>=0 and vry_pos < 3):
    vry_pos=0
  elif(vry_pos>=1000 and vry_pos <=1035):
    vry_pos=1000
  return vry_pos
    
def stabil_vrx_2(vrx_pos_2):
  if(vrx_pos_2>=518 and vrx_pos_2 <=528):
    vrx_pos_2=500
  elif (vrx_pos_2>=0 and vrx_pos_2 < 3):
    vrx_pos_2=0
  elif (vrx_pos_2>=1000 and vrx_pos_2<=1030):
    vrx_pos_2=1000
  return vrx_pos_2

def stabil_vry_2(vry_pos_2):
  if(vry_pos_2>=501 and vry_pos_2<=511):
    vry_pos_2=500
  elif (vry_pos_2>=0 and vry_pos_2<=5):
    vry_pos_2=0
  elif (vry_pos_2>=1000 and vry_pos_2<=1030):
    vry_pos_2=1000
  return vry_pos_2 

def run():
  spi_left=set_spi(0)
  spi_right=set_spi(1)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.connect((HOST, PORT))
  swt_channel = 0  
  vrx_channel = 1  
  vry_channel = 2  
  swt_channel_2 = 0  
  vrx_channel_2 = 1  
  vry_channel_2 = 2  

  delay = 0.1
  degree=20


  while True:
    vrx_pos = ReadChannel(vrx_channel,spi_left)  
    vry_pos =abs (ReadChannel(vry_channel,spi_left)-1022)
    swt_val = ReadChannel(swt_channel,spi_left)  
    vrx_pos_2 = ReadChannel(vrx_channel_2,spi_right)  
    vry_pos_2 = abs(ReadChannel(vry_channel_2,spi_right) -1023)
    swt_val_2 = ReadChannel(swt_channel_2,spi_right)  
 
    vrx_pos=float((stabil_vrx(vrx_pos)-500)/500)
    vry_pos=float(stabil_vry(vry_pos)/1000)
    vrx_pos_2=float((stabil_vrx_2(vrx_pos_2)-500)/500)
    vry_pos_2=float((stabil_vry_2(vry_pos_2)-500)/500)
    if(swt_val>700) :
      mode="0"
    else:
      mode="1"
    msg=f"{vrx_pos} {vry_pos} {vrx_pos_2} {vry_pos_2} "+mode  #yaw throtle  roll pirch
    #print(msg)
    sock.sendto(msg.encode(),(HOST,PORT))
    time.sleep(delay)
def run_recv():
  sock_2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  
  UDP_IP = "192.168.50.52"  #내가 받을곳
  UDP_PORT = 8005

  sock_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock_2.bind((UDP_IP, UDP_PORT))

  s = [b'\xff' * 11520 for x in range(20)]

  fourcc = cv2.VideoWriter_fourcc(*'DIVX')
  out = cv2.VideoWriter('output.avi', fourcc, 25.0, (320,240))  #320 240  640   480
  while True:
      picture = b''
      data, addr = sock_2.recvfrom(11521)  #46081
      s[data[0]] = data[1:11521]

      if data[0] == 19:
          for i in range(20):
              picture += s[i]

          frame = numpy.fromstring(picture, dtype=numpy.uint8)
          frame = frame.reshape(240, 320,3)
          cv2.imshow("frame", frame)
          out.write(frame)

          if cv2.waitKey(1) & 0xFF == ord('q'):
              cv2.destroyAllWindows()
              break




thread_b=Thread(target=run_recv)
thread_a=Thread(target=run)
thread_b.start()
thread_a.start()