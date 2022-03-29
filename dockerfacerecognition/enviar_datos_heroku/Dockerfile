FROM ubuntu:latest

WORKDIR app

COPY . .
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Caracas" apt-get install curl ffmpeg libsm6 libxext6 python3-pip libpq-dev python3-dev  -y
RUN pip3 install psycopg2
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
RUN pip3 install cloudinary

CMD ["python3", "codigo.py"]

#SE DEBE INSTALAR CLOUDINARY PARA TRAER LAS IMAGENES!!
