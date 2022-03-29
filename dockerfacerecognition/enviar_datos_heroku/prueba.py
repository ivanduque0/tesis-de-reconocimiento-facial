import cloudinary
import cv2
import urllib.request
import numpy as np

cloudinary.config( 
  cloud_name = 'dhvdt2wsd', 
  api_key = '984476536665388', 
  api_secret = 's4pymShC9UrS0Ma3qBrTIkV-nrg',
  secure = True
)
while True:
    url = cloudinary.utils.cloudinary_url('media/personas/27488274_u3j7r9')
    url=url[0]
    imagenurl = urllib.request.urlopen (url) #abrimos el URL
    imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
    foto = cv2.imdecode (imagenarray,-1)
    #print(foto)
    print(foto)



# https://res.cloudinary.com/dhvdt2wsd/image/upload/v1648582058/media/personas/27488274_u3j7r9.jpg