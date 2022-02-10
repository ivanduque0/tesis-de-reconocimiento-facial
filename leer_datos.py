import psycopg2
import pandas


try:
    #aqui se establece la coenxion con la base de datos
    conn = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="localhost", port="5432"
    )
    df = pandas.read_sql('SELECT * FROM pruebapython', conn)

    print(df)

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        conn.close()
        print("se ha cerrado la conexion a la base de datos")