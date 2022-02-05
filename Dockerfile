FROM ubuntu:latest

WORKDIR /dockertensorflow

COPY . .
RUN apt-get update
RUN apt-get install -y nano
RUN apt-get install python3  -y
RUN apt-get install -y python3-pip
RUN pip3 install tflite_runtime
RUN pip3 install mediapipe
RUN pip3 install opencv-contrib-python
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Caracas" apt-get install ffmpeg libsm6 libxext6  -y
CMD ["python3", "/dockertensorflow/probar_modelos_tflite.py"]
