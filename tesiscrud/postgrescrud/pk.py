
cedulafiltro=1
fechadesdefiltro=2
fechahastafiltro=None
horadesdefiltro=4
horahastafiltro=5
listafiltros=[cedulafiltro,fechadesdefiltro,fechahastafiltro,horadesdefiltro,horahastafiltro]
listaindex=[]
#print(listafiltros)

consultasdic=['cedula','fecha__gte','fecha__lte','hora__gte','hora__lte']

for filtro in listafiltros:
    index = listafiltros.index(filtro)
    #print(index)
    if filtro != None:
        listaindex.append(index)

print(listaindex)