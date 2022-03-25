import RPi.GPIO as GPIO
import time
import psycopg2

GPIO.cleanup()
# Primero se configuran los pines
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setwarnings(False)

# Tiempo de encendido
tiempo = 2 #Time interval in Seconds

conn = None
try:  
    conn = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="192.168.21.101", port="4443"
    )
    conn.autocommit = False
    cursor = conn.cursor()

    while True:
        cursor.execute('SELECT * FROM led')
        led_onoff = cursor.fetchall()

        if led_onoff[0][0] == 1:
            print("si reconocio")
            GPIO.output(3, True)
            time.sleep(tiempo)
            GPIO.output(3, False)
            cursor.execute('''UPDATE led SET onoff=0 WHERE onoff=1;''')
            conn.commit()

        if led_onoff[0][0]==2:
            print("no reconocio")
            GPIO.output(5, True)
            time.sleep(tiempo)
            GPIO.output(5, False)
            cursor.execute('''UPDATE led SET onoff=0 WHERE onoff=2;''')
            conn.commit()

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")
    GPIO.cleanup()

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")
        GPIO.cleanup()
