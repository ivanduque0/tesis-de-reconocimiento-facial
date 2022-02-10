import psycopg2
import pandas


try:
    #aqui se establece la coenxion con la base de datos
    conn = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="localhost", port="5432"
    )
    cursor = conn.cursor()

    # cuando se visualizan las consultas en pandas se
    #ve como una lista en psql
    df = pandas.read_sql('SELECT * FROM pruebapython', conn)
    print(df)

    print("\n")
    #----------------------------------------------

    #cuando se usa este codigo solo se pueden ver las
    #filas con sus valores en forma de tuplas y todas van
    #en una lista
    cursor.execute('SELECT * FROM pruebapython')

    #aqui en especifico se colocan todas las filas
    #en forma de tuplas
    #en una lista que va a estar en una variable
    abr = cursor.fetchall()

    #con esto solo se ve la cantidad de filas como
    #un solo numero
    print((len(abr)))
    
    #aqui se ven las filas como tuplas
    print(abr)

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        conn.close()
        print("se ha cerrado la conexion a la base de datos")