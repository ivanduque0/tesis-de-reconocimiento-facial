import cv2
import numpy as np
import os #libreria para crear directorios
import mediapipe as mp
from math import  acos,degrees
import time

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#primero se asegura que no esta creada la carpeta
if not os.path.exists('ivannuevas'):
    #con este metodo se crea una carpeta
    os.makedirs('ivannuevas')

if not os.path.exists('erikaaaa'):
    #con este metodo se crea una carpeta
    os.makedirs('erikaaaa')

contador = 0
contadorr = 0
with mp_face_detection.FaceDetection(
    min_detection_confidence=0.8) as face_detection:
    
    while True:

        ret,video = camara.read()
        video = cv2.flip(video, 0)
        videorgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        alto, ancho, _ = video.shape
        results = face_detection.process(videorgb)

        if results.detections is not None:
            for detection in results.detections:
                
                
                #deteccion de coordenadas de ojo 1
                x1 =int(detection.location_data.relative_keypoints[0].x * ancho)
                y1 =int(detection.location_data.relative_keypoints[0].y * alto)
                
                #deteccion de coordenadas de ojo 2
                x2 =int(detection.location_data.relative_keypoints[1].x * ancho)
                y2 =int(detection.location_data.relative_keypoints[1].y * alto)

                #creando coordenadas de cada punto
                p1 = np.array([x1, y1])
                p2 = np.array([x2, y2])
                p3 = np.array([x2, y1])

                #obteniendo distancias entre los puntos
                d1 = np.linalg.norm(p1-p2)
                d2 = np.linalg.norm(p1-p3)

                angulo = degrees(acos(d2/d1))
                
                #haciendo que el angulo sea negativo cuando se rote la cabeza
                #a la derecha
                if y1 < y2:
                    angulo= -angulo

                #registrando la rotacion
                m = cv2.getRotationMatrix2D((ancho // 2, alto // 2), -angulo, 1)
                
                #crearndo nueva ventana y dandole la rotacion a la imagen
                alinear = cv2.warpAffine(video, m, (ancho,alto))
                #cv2.imshow("alinear", alinear)


                xmin = int(detection.location_data.relative_bounding_box.xmin * ancho)
                ymin = int(detection.location_data.relative_bounding_box.ymin * alto)
                w = int(detection.location_data.relative_bounding_box.width * ancho)
                h = int(detection.location_data.relative_bounding_box.height * alto)

                if xmin < 0 or ymin < 0:
                    continue

                vista_previa = alinear[ymin : ymin + h, xmin : xmin + w]

               
                cv2.imshow("vista previa", vista_previa)


                
                if cv2.waitKey(1) & 0xFF == ord('i'):

                    
                    cv2.imwrite(f'ivannuevas/rostrocortado{contador}.jpg',vista_previa)
                    #cv2.imwrite(f'erikaaaa/rostrocompleto{contador}.jpg',video)
                    cv2.imshow('rostro guardado',vista_previa)

                    print(contador)
                    contador=contador+1
                    #cv2.imwrite(f'C:/Users/ivan/Desktop/tensorflow/ivanuevas/rostrocompleto{contador}.jpg',video)
                    #cv2.imshow('rostro guardado',video)

                    #print(contadorr)
                    #contadorr=contadorr+1
                    
                        
                        

                        

                #if cv2.waitKey(1) & 0xFF == ord('e'):
                    #cv2.imwrite(f'erika/rostro{contadorr}.jpg',vista_previa)
                    #cv2.imshow('rostro guardado',vista_previa)
                    #contadorr=contadorr+1
                    
                    

                

        
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
        cv2.imshow('imagenn', video)
        



camara.release()
cv2.destroyAllWindows()