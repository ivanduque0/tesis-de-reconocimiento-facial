import cv2
import tensorflow as tf
import numpy as np
import mediapipe as mp
from math import  acos,degrees
import os
import matplotlib.pyplot as plt
import urllib.request

nombres = ["erika", "ivan", "diego"]
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
url = 'http://192.168.21.102/cam-hi.jpg'

modelo = tf.keras.models.load_model("modelo iv-er-di conv2d (256,256,256) colab 300x300")



def preparar(imagen):
    matriz_imagen = cv2.imread(imagen, cv2.IMREAD_GRAYSCALE)  # lee la imagen y la convierte a escala de grises
    #cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
    nueva_matriz_imagen = cv2.resize(matriz_imagen, (300, 300))  # redimensiona la imagen
    return nueva_matriz_imagen.reshape(-1, 300, 300, 1)  # retorna la imagen comos e supone que fue entrenado el modelo



with mp_face_detection.FaceDetection(
    min_detection_confidence=0.7) as face_detection:
    
    with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75) as face_mesh:
    
        while True:

            imagenurl = urllib.request.urlopen (url) #abrimos el URL
            imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
            video = cv2.imdecode (imagenarray,-1) #decodificamos
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

                    #cv2.imshow("vista previa", vista_previa) 
                    #cv2.imshow("vista previa", alinear)

                    alineargb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                    
                    results2 = face_mesh.process(videorgb)   


                                    
                    #if results2.multi_face_landmarks is not None:
                     #   for face_landmarks in results2.multi_face_landmarks:
                      #      mp_drawing.draw_landmarks(video, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1))
                                # FACEMESH_TESSELATION CONTOURS


                    cv2.imwrite(f'rostrorver.jpg', vista_previa)
                    cv2.imshow("vista previa", vista_previa) 
                    
                    #cv2.line(video,(xmin,ymin),(xmin,ymin+60),(255,0,0),5)
                    #cv2.circle(video, (xmin,ymin), 2, (255, 0, 255),2)

                    prediccion = modelo.predict([preparar('rostrorver.jpg')])
                    print(prediccion)
                    prediccion=np.array(prediccion)
                    #print(nombres[int(prediccion[0][0])])
                    
                    if prediccion[0,0] >= 0.8:
                        print(nombres[0])
                        cv2.line(video,(xmin,ymin),(xmin+60,ymin),(0,0,255),5)
                        cv2.line(video,(xmin,ymin),(xmin,ymin+60),(0,0,255),5)
                        cv2.line(video,(xmin + w,ymin),(xmin+w-60,ymin),(0,0,255),5)
                        cv2.line(video,(xmin + w,ymin),(xmin+w,ymin+60),(0,0,255),5)
                        cv2.line(video,(xmin,ymin+h),(xmin,ymin+h-60),(0,0,255),5)
                        cv2.line(video,(xmin,ymin+h),(xmin+60,ymin+h),(0,0,255),5)
                        cv2.line(video,(xmin + w,ymin+h),(xmin+w,ymin+h-60),(0,0,255),5)
                        cv2.line(video,(xmin + w,ymin+h),(xmin+w-60,ymin+h),(0,0,255),5)
                        cv2.putText(video, "erika", (xmin,ymin),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                    if prediccion[0,1] >= 0.8:
                        print(nombres[1])
                        cv2.line(video,(xmin,ymin),(xmin+60,ymin),(255,0,0),5)
                        cv2.line(video,(xmin,ymin),(xmin,ymin+60),(255,0,0),5)
                        cv2.line(video,(xmin + w,ymin),(xmin+w-60,ymin),(255,0,0),5)
                        cv2.line(video,(xmin + w,ymin),(xmin+w,ymin+60),(255,0,0),5)
                        cv2.line(video,(xmin,ymin+h),(xmin,ymin+h-60),(255,0,0),5)
                        cv2.line(video,(xmin,ymin+h),(xmin+60,ymin+h),(255,0,0),5)
                        cv2.line(video,(xmin + w,ymin+h),(xmin+w,ymin+h-60),(255,0,0),5)
                        cv2.line(video,(xmin + w,ymin+h),(xmin+w-60,ymin+h),(255,0,0),5)
                        cv2.putText(video, "ivan", (xmin,ymin),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
                    if prediccion[0,2] >= 0.8:
                        print(nombres[2])
                        cv2.line(video,(xmin,ymin),(xmin+60,ymin),(0, 255, 0),5)
                        cv2.line(video,(xmin,ymin),(xmin,ymin+60),(0, 255, 0),5)
                        cv2.line(video,(xmin + w,ymin),(xmin+w-60,ymin),(0, 255, 0),5)
                        cv2.line(video,(xmin + w,ymin),(xmin+w,ymin+60),(0, 255, 0),5)
                        cv2.line(video,(xmin,ymin+h),(xmin,ymin+h-60),(0, 255, 0),5)
                        cv2.line(video,(xmin,ymin+h),(xmin+60,ymin+h),(0, 255, 0),5)
                        cv2.line(video,(xmin + w,ymin+h),(xmin+w,ymin+h-60),(0, 255, 0),5)
                        cv2.line(video,(xmin + w,ymin+h),(xmin+w-60,ymin+h),(0, 255, 0),5)
                        cv2.putText(video, "diego", (xmin,ymin),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                        
        
            cv2.imshow('imagenn', video)
            if cv2.waitKey(1) & 0xFF == 27:
                break

         
cv2.destroyAllWindows()


