FROM arm32v7/python:3.8.12

WORKDIR leds

COPY . .
RUN pip3 install --no-cache-dir rpi.gpio
RUN alias python=python3
RUN pip3 install psycopg2
CMD ["python3", "blinkraspberry.py"]
