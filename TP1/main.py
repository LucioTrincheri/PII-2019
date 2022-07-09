import os

# Funcion para sacar el path completo al directorio (para compatibilidad entre SO)
def openFile(name, mode):
    _location_ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return open((os.path.join(_location_, name)), mode)

# Leo el archivo y separo en personas que pueden tener pareja y las que no
def fileParser(url):
    # Inicializo los arrays de diccionarios de personas aceptadas y rechazadas
    posibles = []
    rechazadas = {'edad': [], 'gustos': [], 'noObtuvo': []}
    # Abro el archivo de entrada y compruebo si este se encuentra en modo lectura
    file = openFile(url, "r")
    if file.mode == 'r':
        # Leo las lineas del archivo
        lines = file.readlines()
        # organizacion de la tupla: (nombre, apellido, localidad, edad, sexo, gustos)
        for line in lines:
			# Separo los valores entre comas
            data = line.split(", ")
            # Trasnformo la edad a un integer y borro el salto de linea o retorno
            data[3] = int(data[3])
            data[5] = data[5].rstrip('\n').rstrip('\r')
			# Transformo la array a tupla
            data = tuple(data)
            # Agrego las personas a su array correspondiente segun su edad y gustos
            if ((data[5] != 'N') and (data[3] > 10)):
                if data[5] == 'A':
                    posibles.insert(0, data)
                else:
                    posibles.append(data)
            else:
                if data[5] == 'N':
                    rechazadas["gustos"].append(data)
                else:
                    rechazadas["edad"].append(data)

    # Coloco las personas bisexuales al final del array 
	# ya que pueden relacionarse con cualquiera
    posibles.reverse()
    # Retorno los arrays de candidatos
    file.close()
    return posibles, rechazadas

# Esta fucnion comprueba si dos personas pueden ser pareja
def compatibilidad(p1, p2):
    # Primer determinante, misma localidad
    if(p1[2] == p2[2]):
        # Segundo criterio, edades compatibles, mayores con mayores, menores con menores xD
        if(((p1[3] < 18) and (p2[3] < 18)) or ((p1[3] >= 18) and (p2[3] >= 18))):
            # Tercer criterio, gustos, teniendo encuenta a todos los gustos
            if((p1[5] == 'A' or p1[5] == p2[4]) and (p2[5] == p1[4] or p2[5] == 'A')):
                return True
    return False

# Creo las parejas y agrego la gente rechazada al grupo correspondiente
def crearParejas(lista_personas):
    # Lista de tuplas, que representan a las parejas matcheadas
    resultado = []
    # Lista de personas sin pareja
    rechazado = []
    # Loop que recorrera toda la lista de personas posibles a matchear
    while len(lista_personas) > 0:
        # Bandera que utilizamos para decidir si una persona fue rechazada o se le asigno pareja
        bandera = 0
        # Persona a buscar pareja
        per = lista_personas[0]
        # Contador para recorrer el array
        contPosible = 1
        # Una vez seleccionada una perona recorremos la lista, hasta encontrar una pareja posible
        while contPosible < len(lista_personas):
            # Posible pareja de "per"
            pos = lista_personas[contPosible]
            # Si la funcion compatibilidad nos devuelve True, es decir que esas personas pueden matchear
            if(compatibilidad(per, pos)):
                # Procedemos a agregar a esa pareja a la lista de tuplas reultado
                resultado.append((per, pos))
                # Y eliminamos a las dos de la lista de posibles
                lista_personas.pop(contPosible)
                lista_personas.pop(0)
                # Colocamos la bandera en 1 para indicar que esa persona encontro pareja
                bandera = 1
                break
            contPosible += 1
        # Si la persona no encontro pareja, la bandera seguira en 0 y es agregada a la lista de rechazados
        if bandera == 0:
            rechazado.append(per)
            lista_personas.pop(0)
    return resultado, rechazado

# Escribe las parejas resultantes en el archivo parejas.txt
def writeParejas(parejas):
    # Abrimos el archivo en modo escritura
    salida = openFile('parejas.txt', 'w+')
    # Por cada pareja, escribimos la linea con sus datos segun la forma especificada
    for p in parejas:
        salida.write("%s, %s, %d - %s, %s, %d - %s\n" % (p[0][0], p[0][1], p[0][3], p[1][0], p[1][1], p[1][3], p[0][2]))
    # Cerramos el archivo
    salida.close()

# Escribe las personas rechazadas y el porque en el archivo rechazadas.txt
def writeRechazadas(rechazadas):
    # Abrimos el archivo en modo escritura
    salida = openFile('rechazadas.txt', 'w+')
    # Escribimos las personas que no tienen pareja debajo de la razon correspondiente
    salida.write("Rechazadas por edad:\n\n")
    for r in rechazadas["edad"]:
        salida.write("%s\n" % repr(r).lstrip("(").rstrip(")"))
    salida.write("\n\nRechazadas por gustos:\n\n")
    for r in rechazadas["gustos"]:
        salida.write("%s\n" % repr(r).lstrip("(").rstrip(")"))
    salida.write("\n\n No consiguio pareja:\n\n")
    for r in rechazadas["noObtuvo"]:
        salida.write("%s\n" % repr(r).lstrip("(").rstrip(")"))
    # Cerramos el archivo
    salida.close()


posibles, rechazadas = fileParser("ejemplo1.txt")
resultado, rechazadas["noObtuvo"] = crearParejas(posibles)
writeParejas(resultado)
writeRechazadas(rechazadas)
