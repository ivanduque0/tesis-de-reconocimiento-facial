import face_recognition
import cv2
import numpy as np
import pandas
import psycopg2
import pytz
from datetime import datetime
import os
import time
from math import  acos,degrees
import mediapipe as mp

conn = None
directorio="/home/ivan/Desktop/dockerfacerecognition/personas"
imagenes = os.listdir(directorio)
nombres = []
caras = []
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture("http://192.168.21.102:81/stream")
parpado=0
parpadeos=0
d1old=0
d2old=0
vista_previargb = 0
vista_previa = 0
razon="entrada"
t1=0
t2=0
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

try:

    conn = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="localhost", port="4444"
    )

    conn.autocommit = False
    cursor = conn.cursor()

    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.7) as face_detection:
        
        with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75) as face_mesh:

            while True:
                tz = pytz.timezone('America/Caracas')
                caracas_now = datetime.now(tz)
                
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
                        

                        #if xmin < 0 or ymin < 0:
                        #    continue
                        if ymin >=20 and xmin >= 20:
                            vista_previa = alinear[ymin-20 : ymin + h +20, xmin - 20: xmin + w +20]
                            vista_previargb = cv2.cvtColor(vista_previa, cv2.COLOR_BGR2RGB)
                        alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                        
                        results2 = face_mesh.process(alinear_rgb)
                        
                        if results2.multi_face_landmarks is not None:

                            for face_landmarks in results2.multi_face_landmarks:

                                y_386 = int(face_landmarks.landmark[386].y * alto) 
                                y_374 = int(face_landmarks.landmark[374].y * alto) 
                                y_159 = int(face_landmarks.landmark[159].y * alto)
                                y_145 = int(face_landmarks.landmark[145].y * alto)
                                x_386 = int(face_landmarks.landmark[386].x * ancho) 
                                x_374 = int(face_landmarks.landmark[374].x * ancho) 
                                x_159 = int(face_landmarks.landmark[159].x * ancho)
                                x_145 = int(face_landmarks.landmark[145].x * ancho)

                                y_1 = int(face_landmarks.landmark[1].y * alto)
                                x_1 = int(face_landmarks.landmark[1].x * ancho) 

                            p1 = np.array([x_386, y_386])
                            p2 = np.array([x_386, y_374])
                            p3 = np.array([x_386, y_159])
                            p4 = np.array([x_386, y_145])

                            d1 = np.linalg.norm(p1-p2)
                            d2 = np.linalg.norm(p4-p3)
                            
                            # dify1_1=
                            # dify1_2=

                            if t1 == 0 or (xmin >= xref+5 and xmin <= xref-5 and ymin >= yref+5 and ymin <= yref-5):
                                xref = xmin
                                yref = ymin

                        

                        # if cv2.waitKey(1) & 0xFF == ord('e'):
                        #     razon = "entrada"
            
                        # if cv2.waitKey(1) & 0xFF == ord('s'):
                        #     razon = "salida"

                            dif1 = (d1old*26)/100
                            dif2 = (d2old*26)/100

                            if d1==d1old and d2==d2old:
                                parpado=1
                            t2=time.perf_counter()

                            if d1<=d1old-dif1 and d2<=d2old-dif2 and parpado==1 and xmin <= xref+5 and xmin>=xref-5 and ymin <= yref+5 and ymin >= yref-5:
                                parpadeos=parpadeos+1  
                                print(parpadeos)        
                                #face_locations = face_recognition.face_locations(alinear_rgb)
                                encodingcamara = face_recognition.face_encodings(vista_previargb)          
                                if encodingcamara != []:

                                    encodingcamaraa = face_recognition.face_encodings(vista_previargb)[0]

                                    resultado = face_recognition.compare_faces(caras, encodingcamaraa, tolerance=0.5)

                                    nombre = "rostro no identificado. parpadee otra vez"

                                    if True in resultado:
                                        rostro_encontrado = resultado.index(True)
                                        nombre = nombres[rostro_encontrado]
                                        fecha=str(caracas_now)[:10]
                                        hora=str(caracas_now)[11:16]
                                        cursor.execute('''INSERT INTO interacciones (nombre, fecha, hora, razon)
                                        VALUES (%s, %s, %s, %s);''', (nombre, fecha, hora, razon))
                                        conn.commit()
                                        tabla = pandas.read_sql('SELECT*FROM interacciones', conn)
                                        print(tabla)
                                        print("\n")
                                    print(nombre)

                                parpado=0
                                d1old=0
                                d2old=0
                                
                            if d1 >= d1old:
                                d1old=d1
                                t1=time.perf_counter()
                            if d1 >= d1old:
                                d2old=d1
                            if (t2-t1)>=0.4:
                                d1old=0
                                d2old=0
                                t1=0
                                
                                
                
                tecla = cv2.waitKey(1)

                #esto es solo para simular la entrada y salida para las consultas
                if tecla & 0xFF == 226:
                    razon = "entrada"
                
                if tecla & 0xFF == 225:
                    razon = "salida"
                
                cv2.imshow('imagen', vista_previa)
                cv2.imshow('imagenn', video)
                

                if tecla & 0xFF == 27:
                    break
                
                tecla = 0
    camara.release()
    cv2.destroyAllWindows()

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")
         

