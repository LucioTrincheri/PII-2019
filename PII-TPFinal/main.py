import heapq
import subprocess
import random
# Constante de direcciones
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Funcion que se encarga de leer el archivo de entrada
# y crear una lista bidimensional del laberinto, junto
# con el lugar de incio y el punto de salida


def parserArchivo(pathF):
    # Apertura
    file = open(pathF, 'r')
    # Inicializo el laberinto
    laberinto = []
    # Inicializo los numeros de caracteres y lineas
    nCarac = nLine = 0
    # Inicializo las tuplas de inicio y fin
    inicio = fin = (0, 0)
    # Leo las lineas del archivo
    lines = file.readlines()
    # Por cada linea, borro el salto de linea
    for line in lines:
        nCarac = 0
        line = line.strip('\n').strip('\r')
        laberinto.append([])
        # Recorro caracter por caracter la linea y
        # escribo los valores en el array segun corresponda
        for carac in line:
            if carac == '1':
                laberinto[nLine].append(1)
            else:
                laberinto[nLine].append(0)
            # Ademas, guardo las posiciones de inicio y fin
            if carac == 'I':
                inicio = (nLine, nCarac)
            if carac == 'X':
                fin = (nLine, nCarac)
            nCarac += 1
        nLine += 1
    # Cierro el archivo y retorno los valores
    file.close()
    return laberinto, inicio, fin

# Funcion para calcular la heuristica desde el punto que estoy
# ubicado hasta la posicion final, lo cual permitira tener una
# direccion general de hacia donde moverse, segun la distancia


def heuristica(act, fin):
    # Si su usara pitagoras para hacer la heuristica, el camino sera
    # mas directo hacia la salida, pero en laberintos grandes,
    # las operaciones matematicas se hacen demasiado costosa
    return (abs(fin[0] - act[0]) + abs(fin[1] - act[1]))


# Funcion que retorna si un punto dado esta fuera del rango del array
def fueraDeRango(x, y, size):
    return (x < 0) or (y < 0) or (x > size) or (y > size)

# Funcion que retorna un array con las tuplas de vecinos posibles


def obtenerVecinos(act, lab, size):
    # Inicializo el array de vecinos
    vecinos = []
    # Por cada tupla de direcciones
    for x, y in DIRECCIONES:
        # Creo el nuevo x, y
        nx = act[0] + x
        ny = act[1] + y
        # Compruebo si estan fuera del rango
        if fueraDeRango(nx, ny, size):
            continue
        # Compruebo si es una pared
        if lab[nx][ny] == 1:
            continue
        # Si no se cumplen ninguna de las 2 condiciones anteriores
        # agrego la tupla en cuestion al array de vecinos
        vecinos.append((nx, ny))
    return vecinos

# Funcion que calcula el recorrido hasta el final, usando
# el algoritmo A*


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def aStar(start, goal, lab):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in obtenerVecinos(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristica(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from, cost_so_far
    '''
    # Guardo el ancho/alto del laberinto
    size = len(lab[0]) - 1
    # Inicializo el array de los puntos de la frontera,
    # asi como los diccionarios que contienen la distancia al inicio,
    # la suma de la distancia al inicio sumada a la heuristica, y
    # el diccionario que indica el padre del cual procede un nodo (x, y)
    frontera = []
    desde = {}
    G = {}
    F = {}
    # Agrego los valores del punto de inicio
    frontera.append(ini)
    G[ini] = 0
    F[ini] = heuristica(ini, fin)
    # Mientras el array de la frontera no este vacio
    while frontera:
        actual = None
        actualF = None
        # Busco el punto con menor valor de dist al origen + heuristica
        for posible in frontera:
            # Mucho mejor seria usar una priority queue
            if actual is None or F[posible] <= actualF:
                actual = posible
                actualF = F[posible]
        # Si este punto es el destino, creo el array de retorno al origen
        if actual == fin:
            camino = [actual]
            while actual in desde:
                actual = desde[actual]
                camino.append(actual)
            # Doy vuelta el array de recorrido, de forma que
            # indique de origen a destino
            camino.reverse()
            return camino
        # Remuevo el nodo actual de la frontera y escribo
        # en el laberinto que ya pase por el nodo
        frontera.remove(actual)
        lab[actual[0]][actual[1]] = 2
        # Obtengo los vecinos posibles al nodo
        vecinos = obtenerVecinos(actual, lab, size)
        # Necesario , ya que los vecinos siempre se obtienen
        # en el mismo orden, Este -> Oeste -> Norte -> Sur
        # y al hacer el append, siempre se prioritiza el sur,
        random.shuffle(vecinos)
        # Por cada vecino...
        for vecino in vecinos:
            # Me fijo si ya lo tome en cuenta, en cuyo caso lo ignoro
            if lab[vecino[0]][vecino[1]] == 2:
                continue
            # Calculo su nueva distancia al origen
            posG = G[actual] + 1
            # Si el vecino no esta en el array de frontra lo agrego
            if vecino not in frontera:
                frontera.append(vecino)
            # Si esta en el array de frontera, pero el nuevo recorrido
            # que estamos calculando tiene mas pasos en el guardado
            # anteriormente, se ignora
            else:
                if posG >= G[vecino]:
                    continue
            # En caso contrario se calcula los valores de G y F (G + heuristica)
            desde[vecino] = actual
            G[vecino] = posG
            F[vecino] = G[vecino] + heuristica(vecino, fin)
    # En caso de estar vacio el array de frontera y no haber
    # encontrado un recorrido, entonces el laberinto no tiene
    # solucion y retorno un array vacio.
    return []
    '''

# Funcion que se encarga de escribir los pasos para resolver el laberinto


def escribirPasos(res):
    salida = open('pasos.txt', 'w')
    salida.write(
        "Pasos escritos de la forma: (Fila, Columna), contando desde la esquina superior izquierda\n")
    for paso in res:
        salida.write("(%d, %d)," % (paso[0] + 1, paso[1] + 1))
    salida.close()


def main():
    # Compilamos el archivo generador.c en un ejecutable
    # Si este paso no es necesario, puede ser borrado
    subprocess.run(["gcc", "generador.c"])
    # Ingreso del nombre del archivo de entrada que generara el laberinto
    entrada = input("Ingrese el nombre del archivo para crear el laberinto: ")
    # Inicializo la variable del resultado
    came = {}
    # Mientras que el resultado retornado por aStar sea vacio,
    # seguiremos llamando al ejecutable para que cree un nuevo
    # laberinto y se volvera a intentar calcular un camino.
    while not resultado:
        # Si al invocar gcc se le da otro nombre al ejecutable y se borra la
        # linea 151, sera necesario cambiar a.out por el nombre del ejecutable
        subprocess.run(["./a.out", entrada])
        laberinto, inicio, fin = parserArchivo("laberinto.txt")
        resultado = aStar(inicio, fin, laberinto)
    # Escribo los pasos para llegar a la salida
    escribirPasos(resultado)


# Llamo al main
if __name__ == "__main__":
    main()
