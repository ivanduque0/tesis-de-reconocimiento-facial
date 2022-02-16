import cv2
import numpy as np
import os #libreria para crear directorios
import mediapipe as mp
from math import  acos,degrees

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
directorio="/home/ivan/Downloads/lfw-deepfunneled"
carpetas = os.listdir(directorio)

with mp_face_detection.FaceDetection(
    min_detection_confidence=0.8) as face_detection:

    for carp in carpetas[:500]:
        ruta = os.path.join(directorio, carp)
        imagenes=os.listdir(ruta)
        ruta2=os.path.join(ruta, imagenes[0])
        print(ruta2)
        print(imagenes[0])
        imagen = cv2.imread(ruta2)
        print(imagen.shape)
        cv2.imshow('imagenn', imagen)
        alto, ancho, _ = imagen.shape
        results = face_detection.process(imagen)

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
                
                if y1 < y2:
                    angulo= -angulo

                m = cv2.getRotationMatrix2D((ancho // 2, alto // 2), -angulo, 1)
                
                alinear = cv2.warpAffine(imagen, m, (ancho,alto))
                alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)

                xmin = int(detection.location_data.relative_bounding_box.xmin * ancho)
                ymin = int(detection.location_data.relative_bounding_box.ymin * alto)
                w = int(detection.location_data.relative_bounding_box.width * ancho)
                h = int(detection.location_data.relative_bounding_box.height * alto)

                if xmin < 0 or ymin < 0:
                    continue

                vista_previa = alinear[ymin : ymin + h, xmin : xmin + w]

                vista_previa_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
                #ruta3=os.path.join(carpetas, imagen)
                #print(ruta3)
                cv2.imwrite(f"/home/ivan/Desktop/app/personas/{imagenes[0]}", vista_previa)
                print(f"se imprimio {imagenes[0]}")

