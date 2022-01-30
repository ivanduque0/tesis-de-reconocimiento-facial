import cv2
import numpy as np
import os #libreria para crear directorios
import mediapipe as mp
from math import  acos,degrees
import time
import matplotlib.pyplot as plt

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

directorio = "C:/Users/Ivonne/Desktop/tensorflow/carass/"
rutaguardar = "C:/Users/Ivonne/Desktop/tensorflow/partes del rostro/"
personas = ["erika"]
contador=0
with mp_face_detection.FaceDetection(
    min_detection_confidence=0.8) as face_detection:
    
    with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.75) as face_mesh:

            for persona in personas:
                ruta = os.path.join(directorio, persona)
                class_num = personas.index(persona)
                print(class_num)

                for foto in os.listdir(ruta):
    
                    imagen = cv2.imread(os.path.join(ruta,foto))
                    #matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    #matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    #plt.imshow(imagen, cmap='gray')
                    #plt.show()
                    #print(matriz_redimensionada.shape)
                    
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
                                    y_18 = int(face_landmarks.landmark[18].y * alto)

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
                                    boca = alinear[y_164-20 : y_18+120, x_234 : x_454]
                                    boca_shape = boca.shape
                                    ojo_derecho = alinear[y_282-20 : y_450+3, x_465-13 : x_446+31]
                                    ojo_derecho_shape = ojo_derecho.shape
                                    ojo_izquierdo = alinear[y_52-20 : y_230+3, x_226-31 : x_245+13]
                                    ojo_izquierdo_shape = ojo_izquierdo.shape
                                    frente = alinear[y_10-15 : y_9-10, x_103-15 : x_332+15]
                                    frente_shape=frente.shape
                                    
                                    partes_rostro = [nariz, boca, ojo_derecho, ojo_izquierdo, frente]
                                    

                                    

                                    if  boca_shape[0]>0 and boca_shape[1]>0 and ojo_derecho_shape[0]>0 and ojo_derecho_shape[1]>0 and ojo_izquierdo_shape[0]>0 and ojo_izquierdo_shape[1]>0 and frente_shape[0]>0 and frente_shape[1]>0:
                                        #cv2.imwrite(os.path.join(rutaguardar, persona, f'nariz{contador}.jpg'),nariz)
                                        cv2.imwrite(os.path.join(rutaguardar, persona, f'boca{contador}.jpg'),boca)
                                        #cv2.imwrite(os.path.join(rutaguardar, persona, f'ojo derecho{contador}.jpg'),ojo_derecho)
                                        #cv2.imwrite(os.path.join(rutaguardar, persona, f'ojo izquierdo{contador}.jpg'),ojo_izquierdo)
                                        #cv2.imwrite(os.path.join(rutaguardar, persona, f'frente{contador}.jpg'),frente)
                                        contador=contador+1
                                        print(contador)
                                    

                
                        
            

cv2.destroyAllWindows()