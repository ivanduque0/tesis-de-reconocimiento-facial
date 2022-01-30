import cv2
import mediapipe as mp
import numpy as np
import urllib.request #para abrir y leer URL

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
parpado=0
parpadeos=0
url = 'http://192.168.21.102/cam-hi.jpg'
#url = 'http://192.168.1.6/'

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.75) as face_mesh:
    
    while True:
        imagenurl = urllib.request.urlopen (url) #abrimos el URL
        imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
        video = cv2.imdecode (imagenarray,-1) #decodificamos
        videorgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(videorgb)
        
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(video, face_landmarks, 
                    mp_face_mesh.FACEMESH_TESSELATION, 
                    # FACEMESH_TESSELATION CONTOURS
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1))
        print(type(mp_face_mesh.FACEMESH_TESSELATION))
        cv2.imshow('video', video)
        print(video.shape)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
cv2.destroyAllWindows()