FROM ubuntu:latest

WORKDIR app

COPY . .
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Caracas" apt-get install ffmpeg libsm6 libxext6 python3-opencv python3-pip libpq-dev python3-dev  -y
RUN apt-get install -y vim
RUN pip3 install psycopg2
RUN pip3 install pandas
RUN pip3 install SQLAlchemy
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --no USE_AVX_INSTRUCTIONS
RUN pip3 install pytz
RUN pip3 install mediapipe
RUN pip3 install opencv-contrib-python
RUN pip3 install tflite_runtime
RUN pip3 install -U numpy
RUN pip3 install face_recognition

ENV QT_DEBUG_PLUGINS=1

CMD ["python3", "codigo.py"]
