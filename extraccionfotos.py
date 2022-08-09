import time
import urllib.request
import numpy as np
import cv2
import os

contador=1201
iniciar = 0
# url = 'http://192.168.20.148:8080/?action=snapshot'
# imagenurl = urllib.request.urlopen (url) #abrimos el URL
# imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
# fotovisible = cv2.imdecode (imagenarray,-1)
# camara = cv2.VideoCapture("http://192.168.20.148:8080/?action=stream")
while contador<1501:
    # ret,video = camara.read()
    print(contador)
    url = 'http://192.168.0.126:8080/?action=snapshot'
    imagenurl = urllib.request.urlopen (url) #abrimos el URL
    imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
    video = cv2.imdecode (imagenarray,-1)
    alto, ancho, _ = video.shape
    #print(alto,ancho)
    K = np.float32([[1,0,100],[0,1,100]])
    video2 = cv2.warpAffine(video, K, (ancho+200,alto+200))
    alto2, ancho2, _ = video2.shape
    K = cv2.getRotationMatrix2D((ancho2 // 2, alto2 // 2), 90, 1)
    video2 = cv2.warpAffine(video2, K, (alto2,ancho2))
    K = np.float32([[1,0,-160],[0,1,-41]])
    video3 = cv2.warpAffine(video2, K, (alto, ancho))
    video3 = cv2.flip(video3, 0)

    cv2.imshow('imagen3', video3)
    tecla = cv2.waitKey(1)
    #numerotecla=tecla & 0xFF
    #print(numerotecla)
    if tecla & 0xFF == 105:
        time.sleep(2)
        iniciar=1
    if tecla & 0xFF == 112:
        iniciar=0
    if tecla & 0xFF == 27:
        break
    if iniciar == 1:
        time.sleep(0.5)
        cv2.imwrite(f"/home/seguricel/Desktop/modelo_antispoofing/spoofing/fotosinspoofing/fotosinspoofing{contador}.jpg",video3)
        contador=contador+1
    if tecla & 0xFF == 115:
        time.sleep(0.5)
        cv2.imwrite(f"/home/seguricel/Desktop/modelo_antispoofing/spoofing/fotosinspoofing/fotosinspoofing{contador}.jpg",video3)
        contador=contador+1
    