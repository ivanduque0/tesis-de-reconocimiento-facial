import cv2

video=0
tecla=0
while True:
    cv2.imshow('imagen3', video)
    
    numerotecla=tecla & 0xFF
    print(numerotecla)
    tecla = cv2.waitKey(100)
    
