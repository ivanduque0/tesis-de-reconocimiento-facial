import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.75) as face_mesh:
    
    while True:
        ret,video = camara.read()
        video = cv2.flip(video, 0)
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
    
camara.release()
cv2.destroyAllWindows()