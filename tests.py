from main import parserArchivo, heuristica, fueraDeRango, obtenerVecinos, aStar
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

#def test_fueraDeRango():

#def test_obtenerVecinos():

#def test_aStar():