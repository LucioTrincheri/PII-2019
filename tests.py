from main import parserArchivo, heuristica, fueraDeRango, obtenerVecinos
def test_parserArchivo():
  lab, ini, fin = parserArchivo("test_files/test_parserArchivo.txt")
  res = open("test_files/resultado_parserArchivo.txt", "r")
  lines = res.readlines()
  array = eval(lines[0])
  index = 0
  while index < len(array):
    assert lab[index] == array[index]
    index += 1
  # Posiciones del array, por lo cual tanto a x como a y se le resta 1 
  assert ini == (0, 0)
  assert fin == (4, 3)


def test_heuristica():
  test = open("test_files/test_heuristica.txt", "r")
  resul = open("test_files/resultado_heuristica.txt", "r")
  test_lines = test.readlines() # Tupla inicio \n Tupla fin
  resul_lines = resul.readlines() # Valor de heuristica
  assert heuristica(eval(test_lines[0]), eval(test_lines[1])) == eval(resul_lines[0])
  assert heuristica(eval(test_lines[2]), eval(test_lines[3])) == eval(resul_lines[1])
  assert heuristica(eval(test_lines[4]), eval(test_lines[5])) == eval(resul_lines[2])


def test_fueraDeRango():
  test = open("test_files/test_fueraDeRango.txt", "r")
  resul = open("test_files/resultado_fueraDeRango.txt", "r")
  test_lines = test.readlines() # Tamaño y tuplas a evaluar
  resul_lines = resul.readlines() # Retorno de funcion
  assert fueraDeRango(eval(test_lines[1])[0], eval(test_lines[1])[1], eval(test_lines[0])) == eval(resul_lines[0])
  assert fueraDeRango(eval(test_lines[2])[0], eval(test_lines[2])[1], eval(test_lines[0])) == eval(resul_lines[1])
  assert fueraDeRango(eval(test_lines[3])[0], eval(test_lines[3])[1], eval(test_lines[0])) == eval(resul_lines[2])
  assert fueraDeRango(eval(test_lines[4])[0], eval(test_lines[4])[1], eval(test_lines[0])) == eval(resul_lines[3])


def test_obtenerVecinos():
  lab, ini, fin = parserArchivo("test_files/test_parserArchivo.txt")
  test = open("test_files/test_obtenerVecinos.txt", "r")
  resul = open("test_files/resultado_obtenerVecinos.txt", "r")
  test_lines = test.readlines() # Tupla a buscar vecinos (posiciones de array, osea x - 1, y - 1)
  resul_lines = resul.readlines() # Lista de vecinos (posiciones de array, osea x - 1, y - 1)
  size = 6 #(tamaño de los arrays, osea tamaño real - 1)
  assert obtenerVecinos(eval(test_lines[0]), lab, size) == eval(resul_lines[0])
  assert obtenerVecinos(eval(test_lines[1]), lab, size) == eval(resul_lines[1])
  assert obtenerVecinos(eval(test_lines[2]), lab, size) == eval(resul_lines[2])

# El test de aStar no puede ser realizado, ya que se randomiza la direccion de los vecinos
# Por lo cual el recorrido, aunque se mantiene de distancia minima, varia en algunas situaciones

'''
def test_aStar():
  test = open("test_files/test_aStar.txt", "r")
  resul = open("test_files/resultado_aStar.txt", "r")
  test_lines = test.readlines()
  resul_lines = resul.readlines()
  (ini, fin, lab) = eval(test_lines[0])
  assert aStar(ini, fin, lab) == eval(resul_lines[0])
'''