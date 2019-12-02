import subprocess
import os
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parserArchivo(pathF):
    file = open(pathF, 'r')
    maze = []
    lines = file.readlines()
    nCarac = nLine = 0
    inicio = fin = (0, 0)
    for line in lines:
        nCarac = 0
        line = line.strip('\n').strip('\r')
        maze.append([])
        for carac in line:
            if carac == '1':
                maze[nLine].append(1)
            else:
                maze[nLine].append(0)
            if carac == 'I':
                inicio = (nLine, nCarac)
            if carac == 'X':
                fin = (nLine, nCarac)
            nCarac += 1
        nLine += 1
    file.close()
    return maze, inicio, fin


def heuristica(act, fin):
    return (abs(fin[0] - act[0]) + abs(fin[1] - act[1]))


def fueraDeRango(x, y, size):
    return (x < 0) or (y < 0) or (x > size) or (y > size)


def obtenerVecinos(act, lab, size):
    vecinos = []
    for x, y in DIRECCIONES:
        nx = act[0] + x
        ny = act[1] + y
        if fueraDeRango(nx, ny, size):
            continue
        if lab[nx][ny] == 1:
            continue
        vecinos.append((nx, ny))
    return vecinos


def aStar(ini, fin, lab):
    # Inicializo variables necesarias
    size = len(lab[0]) - 1
    # Arrays de nodos visitados y sin visitar
    frontera = []
    desde = {}
    G = {}
    F = {}
    frontera.append(ini)
    G[ini] = 0
    F[ini] = heuristica(ini, fin)
    while frontera:
        actual = None
        actualF = None
        for posible in frontera:
            if actual is None or F[posible] < actualF:
                actual = posible
                actualF = F[posible]
        if actual == fin:
            camino = [actual]
            while actual in desde:
                actual = desde[actual]
                camino.append(actual)
            camino.reverse()
            return camino
        # Remuevo el nodo actual de la frontera y escribo
        # en el laberinto que ya pase por el nodo
        frontera.remove(actual)
        lab[actual[0]][actual[1]] = 2
        vecinos = obtenerVecinos(actual, lab, size)
        for vecino in vecinos:
            if lab[vecino[0]][vecino[1]] == 2:
                continue
            posG = G[actual] + 1
            if vecino not in frontera:
                frontera.append(vecino)
            else:
                if posG >= G[vecino]:
                    continue
            desde[vecino] = actual
            G[vecino] = posG
            F[vecino] = G[vecino] + heuristica(vecino, fin)
    return []


def escribirPasos(res):
    salida = open('pasos.txt', 'w')
    for paso in res:
        salida.write("(%d, %d)," % (paso[0] + 1, paso[1] + 1))
    salida.close()


def main():
    #subprocess.run(["gcc", "-Wall -o main main.c"])
    entrada = input("Ingrese el nombre del archivo para crear el laberinto: ")
    resultado = []
    laberinto = []
    while not resultado:
        subprocess.run(["./generador", entrada])
        laberinto, inicio, fin = parserArchivo("laberinto.txt")
        resultado = aStar(inicio, fin, laberinto)
    escribirPasos(resultado)


if __name__ == "__main__":
    main()
