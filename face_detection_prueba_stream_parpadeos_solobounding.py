import face_recognition
import cv2
import numpy as np
import mediapipe as mp
from math import  acos,degrees
import os

directorio="C:/Users/Ivonne/Desktop/tensorflow/rostros para facerecognition"
imagenes = os.listdir(directorio)
nombres = []
decodificados = []
for imagen in imagenes:
    nombre = os.path.splitext(imagen)[0]
    nombres.append(nombre)

for imagen in imagenes:
    ruta=os.path.join(directorio,imagen)
    subir_foto = face_recognition.load_image_file(ruta)
    decodificar = face_recognition.face_encodings(subir_foto)[0]
    decodificados.append(decodificar)

mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
parpado=0
parpadeos=0

with mp_face_mesh.FaceMesh(
static_image_mode=False,
max_num_faces=1,
min_detection_confidence=0.75,
min_tracking_confidence=0.75) as face_mesh:

    while True:

        ret,video = camara.read()
        video = cv2.flip(video, 0)
        videorgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        alto, ancho, _ = video.shape
        results2 = face_mesh.process(videorgb)   
        
        
        if results2.multi_face_landmarks is not None:
            for face_landmarks in results2.multi_face_landmarks:

                y_386 = int(face_landmarks.landmark[386].y * alto) 
                y_374 = int(face_landmarks.landmark[374].y * alto) 
                y_159 = int(face_landmarks.landmark[159].y * alto)
                y_145 = int(face_landmarks.landmark[145].y * alto)
                y_55 = int(face_landmarks.landmark[55].y * alto)
                x_55 = int(face_landmarks.landmark[55].x * ancho)
                y_285 = int(face_landmarks.landmark[285].y * alto)
                x_285 = int(face_landmarks.landmark[285].x * ancho)
                y_10 = int(face_landmarks.landmark[10].y * alto)
                y_152 = int(face_landmarks.landmark[152].y * alto)
                x_234 = int(face_landmarks.landmark[234].x * ancho)
                x_454 = int(face_landmarks.landmark[454].x * ancho)
                
                
                p1 = np.array([x_55, y_55])
                p2 = np.array([x_285, y_285])
                p3 = np.array([x_285, y_55])

                d1 = np.linalg.norm(p1-p2)
                d2 = np.linalg.norm(p1-p3)

                angulo = degrees(acos(d2/d1))
                
                #haciendo que el angulo sea negativo cuando se rote la cabeza
                #a la derecha
                if y_55 < y_285:
                    angulo= -angulo

                #registrando la rotacion
                m = cv2.getRotationMatrix2D((ancho // 2, alto // 2), -angulo, 1)

                #creando nueva ventana y dandole la rotacion a la imagen
                alinear = cv2.warpAffine(video, m, (ancho,alto))
                alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)

                p1 = np.array([0, y_386])
                p2 = np.array([0, y_374])
                p3 = np.array([0, y_159])
                p4 = np.array([0, y_145])

                d1 = np.linalg.norm(p2-p1)
                d2 = np.linalg.norm(p4-p3)

                if d1>20 and d2>20:
                    parpado=1

                if d1<=15 and d2<=15 and parpado==1:

                    #caracamara = face_recognition.load_image_file("rostrorver.jpg")
                    face_locations = face_recognition.face_locations(alinear_rgb)
                    encodingcamara = face_recognition.face_encodings(alinear_rgb)
                

                    if encodingcamara != []:

                        encodingcamaraa = face_recognition.face_encodings(alinear_rgb, face_locations)[0]

                        resultado = face_recognition.compare_faces(decodificados, encodingcamaraa, tolerance=0.5)

                        nombre = "rostro no identificado. parpadee otra vez"

                        if True in resultado:
                            rostro_encontrado = resultado.index(True)
                            nombre = nombres[rostro_encontrado]
                        
                        print(nombre)
                         

                    parpado=0
                        
        cv2.imshow('imagenn', video)
        if cv2.waitKey(1) & 0xFF == 27:
            break

         

