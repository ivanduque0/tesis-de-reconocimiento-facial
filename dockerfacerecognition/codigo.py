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
directorio="personas"
imagenes = os.listdir(directorio)
imagenesold=imagenes
nombres = []
caras = []
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
parpado=0
parpadeos=0
d1old=0
d2old=0
vista_previargb = 0
vista_previa = 0
razon="entrada"
t1=time.perf_counter()
t2=0
xref=0
yref=0
xrefold=0
yrefold=0
x_1=0
y_1=0

for imagen in imagenes:
    ruta=os.path.join(directorio,imagen)
    subir_foto = face_recognition.load_image_file(ruta)
    decodificar = face_recognition.face_encodings(subir_foto)
    if decodificar != []:
        decodificar = face_recognition.face_encodings(subir_foto)[0]
        caras.append(decodificar)
        nombre = os.path.splitext(imagen)[0]
        nombres.append(nombre)

caras2 = np.array(caras)
print(caras2.shape)

# for khe in nombres:
#     if khe=="ivan.jpg":
#         print("si estoy xd")

try:

    conn = psycopg2.connect(
        database="tesis2", user="tesis2", password="tesis2", host="postgres", port="5432"
    )

    conn.autocommit = False
    cursor = conn.cursor()


    with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75) as face_mesh:
        #camara = cv2.VideoCapture("http://192.168.21.102:81/stream")
        camara = cv2.VideoCapture("http://192.168.20.102:8080/?action=stream")

        while True:
            tz = pytz.timezone('America/Caracas')
            caracas_now = datetime.now(tz)
            
            ret,video = camara.read()
            #video = cv2.flip(video, 0)
            #print(video)
            if video is not None:
                
                alto, ancho, _ = video.shape
                K = np.float32([[1,0,100],[0,1,100]])
                video2 = cv2.warpAffine(video, K, (ancho+200,alto+200))
                alto2, ancho2, _ = video2.shape
                K = cv2.getRotationMatrix2D((ancho2 // 2, alto2 // 2), 90, 1)
                video2 = cv2.warpAffine(video2, K, (alto2,ancho2))
                K = np.float32([[1,0,-180],[0,1,-21]])
                video = cv2.warpAffine(video2, K, (alto, ancho))
                alto, ancho, _ = video.shape
                videorgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(videorgb)

                if results.multi_face_landmarks is not None:

                    for face_landmarks in results.multi_face_landmarks:
                        
                        #mejilla derecha
                        y_447 = int(face_landmarks.landmark[447].y * alto) 
                        x_447 = int(face_landmarks.landmark[447].x * ancho) 
                        #mejilla izquierda
                        y_227 = int(face_landmarks.landmark[227].y * alto)
                        x_227 = int(face_landmarks.landmark[227].x * ancho)
                        #frente  
                        y_10 = int(face_landmarks.landmark[10].y * alto)
                        x_10 = int(face_landmarks.landmark[10].x * ancho)
                        #barbilla
                        y_175 = int(face_landmarks.landmark[175].y * alto)
                        x_175 = int(face_landmarks.landmark[175].x * ancho)

                    #creando coordenadas de cada punto
                    p1 = np.array([x_447, y_447])
                    p2 = np.array([x_227, y_227])
                    p3 = np.array([x_227, y_447])

                    #obteniendo distancias entre los puntos
                    d1 = np.linalg.norm(p1-p2)
                    d2 = np.linalg.norm(p1-p3)

                    angulo = degrees(acos(d2/d1))
                    
                    #haciendo que el angulo sea negativo cuando se rote la cabeza
                    #a la derecha
                    if y_227 < y_447:
                        angulo= -angulo

                    #registrando la rotacion
                    m = cv2.getRotationMatrix2D((ancho // 2, alto // 2), -angulo, 1)
                    
                    #crearndo nueva ventana y dandole la rotacion a la imagen
                    alinear = cv2.warpAffine(video, m, (ancho,alto))
                    alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                        #cv2.imshow("alinear", alinear)
                        
                    results2 = face_mesh.process(alinear_rgb)
                    
                    if results2.multi_face_landmarks is not None:

                        for face_landmarks in results2.multi_face_landmarks:

                            #puntos de los parpados 
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

                            #mejilla derecha
                            y_447 = int(face_landmarks.landmark[447].y * alto) 
                            x_447 = int(face_landmarks.landmark[447].x * ancho) 
                            #mejilla izquierda
                            y_227 = int(face_landmarks.landmark[227].y * alto)
                            x_227 = int(face_landmarks.landmark[227].x * ancho)
                            #frente  
                            y_10 = int(face_landmarks.landmark[10].y * alto)
                            x_10 = int(face_landmarks.landmark[10].x * ancho)
                            #barbilla
                            y_175 = int(face_landmarks.landmark[175].y * alto)
                            x_175 = int(face_landmarks.landmark[175].x * ancho)
                        

                        #if xmin < 0 or ymin < 0:
                        #    continue
                        if y_10 >=20 and x_227 >= 20:
                            vista_previa = alinear[y_10-20 : y_175 +20, x_227 - 20: x_447 +20]
                            vista_previargb = cv2.cvtColor(vista_previa, cv2.COLOR_BGR2RGB)
                        

                            p1 = np.array([x_386, y_386])
                            p2 = np.array([x_386, y_374])
                            p3 = np.array([x_386, y_159])
                            p4 = np.array([x_386, y_145])

                            d1 = np.linalg.norm(p1-p2)
                            d2 = np.linalg.norm(p4-p3)
                            
                            # dify1_1=
                            # dify1_2=

                            

                            if t2-t1 >= 0.7 and (x_1 >= xref+5 or x_1 <= xref-5 or y_1 >= yref+5 or y_1 <= yref-5):
                                yref = y_1
                                xref = x_1
                            
                            if xrefold != 0 and (xrefold != xref or yrefold != yref):
                                xref=0
                                yref=0
                            
                        # if cv2.waitKey(1) & 0xFF == ord('e'):
                        #     razon = "entrada"
            
                        # if cv2.waitKey(1) & 0xFF == ord('s'):
                        #     razon = "salida"

                            dif1 = (d1old*17)/100
                            dif2 = (d2old*17)/100

                            if d1>=d1old and d2>=d2old:
                                parpado=1
                            t2=time.perf_counter()
                            if t2-t1 < 0:
                                t2=0
                            if d1<=d1old-dif1 and d2<=d2old-dif2 and parpado==1 and x_1 <= xrefold+5 and x_1>=xrefold-5 and y_1 <= yrefold+5 and y_1 >= yrefold-5 and xref == xrefold and yref == yrefold:
                                parpadeos=parpadeos+1         
                                #face_locations = face_recognition.face_locations(alinear_rgb)
                                encodingcamara = face_recognition.face_encodings(vista_previargb)          
                                if encodingcamara != []:

                                    encodingcamaraa = face_recognition.face_encodings(vista_previargb)[0]

                                    resultado = face_recognition.compare_faces(caras, encodingcamaraa, tolerance=0.5)

                                    nombre = "rostro no identificado. parpadee otra vez"

                                    if True in resultado:
                                        rostro_encontrado = resultado.index(True)
                                        cedula_id = nombres[rostro_encontrado]
                                        fecha=str(caracas_now)[:10]
                                        hora=str(caracas_now)[11:16]
                                        cursor.execute('SELECT * FROM postgrescrud_usuarios where cedula=%s', (cedula_id,))
                                        nombrecedula = cursor.fetchall()
                                        if nombrecedula != []:
                                            cedula=nombrecedula[0][0]
                                            nombre=nombrecedula[0][1]
                                            contrato=nombrecedula[0][2]
                                            cursor.execute('''INSERT INTO postgrescrud_interacciones (nombre, fecha, hora, razon, contrato, cedula_id)
                                            VALUES (%s, %s, %s, %s, %s, %s);''', (nombre, fecha, hora, razon, contrato, cedula))
                                            cursor.execute('''UPDATE led SET onoff=1 WHERE onoff=0;''')
                                            conn.commit()
                                            cursor.execute('SELECT * FROM led')
                                            estado_led= cursor.fetchall()
                                            while estado_led[0][0]==1:
                                                cursor.execute('SELECT * FROM led')
                                                estado_led= cursor.fetchall()
                                            #tabla = pandas.read_sql('SELECT*FROM postgrescrud_interacciones', conn)
                                            #print(tabla)
                                            #print("\n")
                                    if nombrecedula == []:
                                        cursor.execute('''UPDATE led SET onoff=2 WHERE onoff=0;''')
                                        conn.commit()
                                        cursor.execute('SELECT * FROM led')
                                        estado_led= cursor.fetchall()
                                        while estado_led[0][0]==2:
                                            cursor.execute('SELECT * FROM led')
                                            estado_led= cursor.fetchall()
                                        
                                    print(nombre)
                                print(f"numero de parpadeos en esta sesion= {parpadeos}")
                                parpado=0
                                d1old=0
                                d2old=0
                                
                            if t2-t1 >= 0.9:
                                d1old=d1
                                d2old=d2
                                t1=time.perf_counter()
                            
                            xrefold=xref
                            yrefold=yref

                                # d2old=0
                                # d1old=0
                            # print("referencias")
                            # print(f"xref={xref}")
                            # print(f"yref={yref}")
                            # print(f"xrefold={xrefold}")
                            # print(f"yrefold={yrefold}")
                            # print("distancias")
                            # print(f"d1={d1}")
                            # print(f"d2={d2}")
                            # print(f"d1old={d1old}")
                            # print(f"d2old={d2old}")
                            # print(f"tiempo={t2-t1}")
                            # print(f"parpadeos={parpadeos}")
                            # print("----------------------------")
                                    
                                
                
                tecla = cv2.waitKey(1)

                #esto es solo para simular la entrada y salida para las consultas
                if tecla & 0xFF == 226:
                    razon = "entrada"
                
                if tecla & 0xFF == 225:
                    razon = "salida"
                
                if tecla & 0xFF == ord('g'):
                    print("ingrese el nombre de la persona a agregar: ") #, end=""
                    nombree = input() # nombre = input("ingrese el nombre de la persona a agregar: ")
                    cv2.imwrite(os.path.join(directorio,f'{nombree}.jpg'),vista_previa)

                    #if tecla & 0xFF == ord('r'):
                    imagenes = os.listdir(directorio)
                    for img in imagenes:
                        try:
                            nombrecarpeta=os.path.splitext(img)[0]         
                            comprobar = nombres.index(nombrecarpeta)
                            #camara.release()
                            #camara = cv2.VideoCapture("http://192.168.20.146:81/stream")

                        except ValueError:
                            ruta=os.path.join(directorio,img)
                            subir_foto = face_recognition.load_image_file(ruta)
                            decodificar = face_recognition.face_encodings(subir_foto)
                            if decodificar != []:
                                decodificar = face_recognition.face_encodings(subir_foto)[0]
                                caras.append(decodificar)
                                nombre = os.path.splitext(img)[0]
                                nombres.append(nombre)
                                print(f"rostro de {nombre} registrado con exito!")
                            #print(nombres)
                            imagenes = os.listdir(directorio)
                            
                    
                    while len(imagenes) != len(nombres):
                                
                                for img in imagenes:
                                    nombre=os.path.splitext(img)[0]
                                    try:
                                        comprobar = nombres.index(nombre)
                                    except ValueError:
                                        ruta=os.path.join(directorio,img)
                                        os.remove(ruta)
                                        imagenes = os.listdir(directorio)
                                        print(f"rostro de {nombre} no registrado!")
                    imagenesold=imagenes


                cv2.imshow('imagen', vista_previa)
                cv2.imshow('imagenn', video)
                

                if tecla & 0xFF == 27:
                    break
                
                tecla = 0
    camara.release()
    cv2.destroyAllWindows()

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")
    camara.release()
    cv2.destroyAllWindows()

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")
        camara.release()
        cv2.destroyAllWindows()