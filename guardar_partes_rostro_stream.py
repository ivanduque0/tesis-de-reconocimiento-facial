import cv2
import numpy as np
import os #libreria para crear directorios
import mediapipe as mp
from math import  acos,degrees
import time

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)



if not os.path.exists('partes del rostro'):
        #con este metodo se crea una carpeta
        os.makedirs('partes del rostro')

directorio = "C:/Users/Ivonne/Desktop/tensorflow/partes del rostro"
personas = ["erika", "ivan", "diego"]


for xd in personas:

        if not os.path.exists(os.path.join('partes del rostro', xd)):
        #con este metodo se crea una carpeta
            os.makedirs(os.path.join('partes del rostro', xd))

contador = 0
contadorr = 0
with mp_face_detection.FaceDetection(
    min_detection_confidence=0.8) as face_detection:
    
    with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.75) as face_mesh:

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
                    alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                    #cv2.imshow("alinear", alinear)


                    xmin = int(detection.location_data.relative_bounding_box.xmin * ancho)
                    ymin = int(detection.location_data.relative_bounding_box.ymin * alto)
                    w = int(detection.location_data.relative_bounding_box.width * ancho)
                    h = int(detection.location_data.relative_bounding_box.height * alto)

                    if xmin < 0 or ymin < 0:
                        continue

                    vista_previa = alinear[ymin : ymin + h, xmin : xmin + w]

                    vista_previa_rgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

                    results2 = face_mesh.process(alinear_rgb)

                    
                    if results2.multi_face_landmarks is not None:

                        for face_landmarks in results2.multi_face_landmarks:

                            #mp_drawing.draw_landmarks(alinear, face_landmarks, 
                            #mp_face_mesh.FACEMESH_TESSELATION, 
                            # FACEMESH_TESSELATION CONTOURS
                            #mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                            #mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1))
                            
                            #coordenadas de la nariz
                            y_164 = int(face_landmarks.landmark[164].y * alto) 
                            x_423 = int(face_landmarks.landmark[423].x * ancho)
                            x_203 = int(face_landmarks.landmark[203].x * ancho)
                            y_195 = int(face_landmarks.landmark[195].y * alto)

                            #coordenadas de la boca
                            x_234 = int(face_landmarks.landmark[234].x * ancho)
                            x_454 = int(face_landmarks.landmark[454].x * ancho)
                            y_152 = int(face_landmarks.landmark[152].y * alto)

                            #coordenadas del ojo derecho
                            y_450 = int(face_landmarks.landmark[450].y * alto) 
                            x_446 = int(face_landmarks.landmark[446].x * ancho)
                            x_465 = int(face_landmarks.landmark[465].x * ancho)
                            y_282 = int(face_landmarks.landmark[282].y * alto)

                            #coordenadas del ojo izquierdo
                            y_230 = int(face_landmarks.landmark[230].y * alto) 
                            x_245 = int(face_landmarks.landmark[245].x * ancho)
                            y_52 = int(face_landmarks.landmark[52].y * alto)
                            x_226 = int(face_landmarks.landmark[226].x * ancho)

                            #coordenadas de la frente
                            y_10 = int(face_landmarks.landmark[10].y * alto) 
                            x_103 = int(face_landmarks.landmark[103].x * ancho)
                            y_9 = int(face_landmarks.landmark[9].y * alto) 
                            x_332 = int(face_landmarks.landmark[332].x * ancho)

                            #nariz
                            #cv2.rectangle(alinear, (x_423,y_164+5), (x_203,y_195-15), (0,255,255), 2)

                            #boca
                            #cv2.rectangle(alinear, (x_216,y_164), (x_436,y_18+10), (0,255,255), 2)

                            #ojo derecho
                            #cv2.rectangle(alinear, (x_446+31,y_450+3), (x_465-13,y_282-20), (255,255,255), 2)

                            #ojo izquierdo
                            #cv2.rectangle(alinear, (x_245+13, y_230+3), (x_226-31,y_52-20), (0,255,255), 2)

                            #frente
                            #cv2.rectangle(alinear, (x_103-15, y_10-15), (x_332+15, y_9-10), (0,255,255), 2)
                            
                            
                            nariz = alinear[y_195-15 : y_164+5, x_203 : x_423]
                            nariz_shape = nariz.shape
                            boca = alinear[y_164-20 : y_152+30, x_234-20 : x_454+20]
                            boca_shape = boca.shape
                            ojo_derecho = alinear[y_282-20 : y_450+3, x_465-13 : x_446+31]
                            ojo_derecho_shape = ojo_derecho.shape
                            ojo_izquierdo = alinear[y_52-20 : y_230+3, x_226-31 : x_245+13]
                            ojo_izquierdo_shape = ojo_izquierdo.shape
                            frente = alinear[y_10-15 : y_9-10, x_103-15 : x_332+15]
                            frente_shape=frente.shape
                            
                            partes_rostro = [nariz, boca, ojo_derecho, ojo_izquierdo, frente]

                            if frente_shape[0]>0 and frente_shape[1]>0:
                                cv2.imshow('nariz', nariz)

                            if boca_shape[0]>0 and boca_shape[1]>0:
                                cv2.imshow('boca', boca)

                            if ojo_derecho_shape[0]>0 and ojo_derecho_shape[1]>0:
                                cv2.imshow('ojo derecho', ojo_derecho)

                            if ojo_izquierdo_shape[0]>0 and ojo_izquierdo_shape[1]>0:
                                cv2.imshow('ojo izquierdo', ojo_izquierdo)

                            if frente_shape[0]>0 and frente_shape[1]>0:
                                cv2.imshow('frente', frente)

                            #xdd = cv2.waitKey(1) 
                            #print(xdd)

                            if cv2.waitKey(1) & 0xFF == 102:
                                if frente_shape[0]>0 and frente_shape[1]>0 and boca_shape[0]>0 and boca_shape[1]>0 and ojo_derecho_shape[0]>0 and ojo_derecho_shape[1]>0 and ojo_izquierdo_shape[0]>0 and ojo_izquierdo_shape[1]>0 and frente_shape[0]>0 and frente_shape[1]>0:
                                    #cv2.imwrite(os.path.join(directorio, personas[1], f'nariz{contador}.jpg'),nariz)
                                    cv2.imwrite(os.path.join(directorio, personas[1], f'boca{contador}.jpg'),boca)
                                    # cv2.imwrite(os.path.join(directorio, personas[1], f'ojo derecho{contador}.jpg'),ojo_derecho)
                                    # cv2.imwrite(os.path.join(directorio, personas[1], f'ojo izquierdo{contador}.jpg'),ojo_izquierdo)
                                    # cv2.imwrite(os.path.join(directorio, personas[1], f'frente{contador}.jpg'),frente)
                                    contador=contador+1
                                    print(contador)
                            

                            cv2.imshow('vista previa', vista_previa)
                            #cv2.imshow('imagen', alinear)

            cv2.imshow('stream', video)
            if cv2.waitKey(1) & 0xFF == 27:
                break
                
            #cv2.imshow('imagen', video)
            
        



camara.release()
cv2.destroyAllWindows()