import face_recognition
import cv2
import tensorflow as tf
import numpy as np
import mediapipe as mp
from math import  acos,degrees
import os

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
directorio="C:/Users/seguricell/Desktop/tensorflow/rostros para face recognition"
imagenes = os.listdir(directorio)
nombres = []
caras = []

for imagen in imagenes:
    nombre = os.path.splitext(imagen)[0]
    print(nombre)
    nombres.append(nombre)

for imagen in imagenes:
    ruta=os.path.join(directorio,imagen)
    print(imagen)
    subir_foto = face_recognition.load_image_file(ruta)
    decodificar = face_recognition.face_encodings(subir_foto)[0]
    caras.append(decodificar)
ruta = "C:/Users/seguricell/Desktop/tensorflow/erikamasfotos"


with mp_face_detection.FaceDetection(
    min_detection_confidence=0.7) as face_detection:
    
    for foto in os.listdir(ruta):

        imagen = cv2.imread(os.path.join(ruta,foto))

        alto, ancho, _ = imagen.shape
        imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = face_detection.process(imagenrgb)
        print(foto)

        if results.detections is not None:
            for detection in results.detections:
                #mp_drawing.draw_detection(video, detection, 
                    #mp_drawing.DrawingSpec(color=(0, 255, 255), circle_radius=5), 
                    #mp_drawing.DrawingSpec(color=(255, 0, 255)))
                
                
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
                alinear = cv2.warpAffine(imagen, m, (ancho,alto))
                #cv2.imshow("alinear", alinear)


                xmin = int(detection.location_data.relative_bounding_box.xmin * ancho)
                ymin = int(detection.location_data.relative_bounding_box.ymin * alto)
                w = int(detection.location_data.relative_bounding_box.width * ancho)
                h = int(detection.location_data.relative_bounding_box.height * alto)

                punto_izquierda = np.array([xmin, ymin])
                punto_derecha = np.array([w, ymin])
                punto_abajo = np.array([xmin, h])

                altura = h - ymin
                largo = w - xmin
                

                if xmin < 0 or ymin < 0:
                    continue

                vista_previa = alinear[ymin : ymin + h, xmin: xmin + w]
                vista_previargb = cv2.cvtColor(vista_previa, cv2.COLOR_BGR2RGB)
                #cv2.imwrite('rostrorver.jpg', vista_previargb)
                #cv2.imshow("vista previa", vista_previa) 
                #caracamara = face_recognition.load_image_file("rostrorver.jpg")
                face_locations = face_recognition.face_locations(imagen)
                encodingcamara = face_recognition.face_encodings(imagen)
                

                if encodingcamara != []:
                    encodingcamaraa = face_recognition.face_encodings(imagenrgb, face_locations)[0]

                    resultado = face_recognition.compare_faces(caras, encodingcamaraa, tolerance=0.50)
                    # print(f" es ivan = {resultado[1]}")
                    # print(f" es erika = {resultado[0]}")
                
                    if resultado[0]:
                        print(nombres[0])

                    if resultado[1]:
                        print(nombres[1])

                    if resultado[2]:
                        print(nombres[2])
