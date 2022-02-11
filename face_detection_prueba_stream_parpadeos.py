import face_recognition
import cv2
import numpy as np
import mediapipe as mp
from math import  acos,degrees
import os

directorio="/home/ivan/Desktop/dockerfacerecognition/personas"
imagenes = os.listdir(directorio)
nombres = []
caras = []
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
parpado=0
parpadeos=0
d1old=0
d2old=0

for imagen in imagenes:
    nombre = os.path.splitext(imagen)[0]
    nombres.append(nombre)

for imagen in imagenes:
    ruta=os.path.join(directorio,imagen)
    subir_foto = face_recognition.load_image_file(ruta)
    decodificar = face_recognition.face_encodings(subir_foto)[0]
    caras.append(decodificar)

caras2 = np.array(caras)
print(caras2.shape)

with mp_face_detection.FaceDetection(
    min_detection_confidence=0.7) as face_detection:
    
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
            results = face_detection.process(videorgb)
            

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
                    alinear = cv2.warpAffine(video, m, (ancho,alto))
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
                    alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                    
                    results2 = face_mesh.process(alinear_rgb)
                    
                    if results2.multi_face_landmarks is not None:

                        for face_landmarks in results2.multi_face_landmarks:

                            y_386 = int(face_landmarks.landmark[386].y * alto) 
                            y_374 = int(face_landmarks.landmark[374].y * alto) 
                            y_159 = int(face_landmarks.landmark[159].y * alto)
                            y_145 = int(face_landmarks.landmark[145].y * alto)

                        p1 = np.array([0, y_386])
                        p2 = np.array([0, y_374])
                        p3 = np.array([0, y_159])
                        p4 = np.array([0, y_145])

                        d1 = np.linalg.norm(p2-p1)
                        d2 = np.linalg.norm(p4-p3)
                        
                        #print(d1)
                        #print(d2)

                        dif1 = (d1old*27)/100
                        dif2 = (d2old*27)/100

                        if d1==d1old and d2==d2old:
                            parpado=1
                        
                        if d1<=d1old-dif1 and d2<=d2old-dif2 and parpado==1:
                            parpadeos=parpadeos+1  
                            print(parpadeos)        
                            face_locations = face_recognition.face_locations(alinear_rgb)
                            encodingcamara = face_recognition.face_encodings(alinear_rgb)          
                            if encodingcamara != []:

                                encodingcamaraa = face_recognition.face_encodings(alinear_rgb, face_locations)[0]

                                resultado = face_recognition.compare_faces(caras, encodingcamaraa, tolerance=0.5)

                                nombre = "rostro no identificado. parpadee otra vez"

                                if True in resultado:
                                    rostro_encontrado = resultado.index(True)
                                    nombre = nombres[rostro_encontrado]
                                
                                print(nombre)

                            parpado=0
                            d1old=0
                            d2old=0

                        if d1 >= d1old:
                            d1old=d1
                        if d1 >= d1old:
                            d2old=d1

            cv2.imshow('imagenn', video)
            if cv2.waitKey(1) & 0xFF == 27:
                break

         

