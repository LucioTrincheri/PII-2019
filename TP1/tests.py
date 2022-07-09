from main import fileParser, compatibilidad, crearParejas, openFile


def test_fileParser():
    pos, rec = fileParser("tests_files/test_fileParser.txt")
    res = openFile("tests_files/resultado_fileParser.txt", "r")
    lines = res.readlines()
    assert pos == eval(lines[0])
    assert rec == eval(lines[1])


def test_compatibilidad():
    pos, rec = fileParser("tests_files/test_compatibilidad.txt")
    res = openFile("tests_files/resultado_compatibilidad.txt", "r")
    lines = res.readlines()
    assert compatibilidad(pos[0], pos[1]) == eval(lines[0])
    assert compatibilidad(pos[0], pos[2]) == eval(lines[1])
    assert compatibilidad(pos[0], pos[3]) == eval(lines[2])
    assert compatibilidad(pos[0], pos[4]) == eval(lines[3])
    assert compatibilidad(pos[2], pos[5]) == eval(lines[4])
    res.close()


def test_crearParejas():
    pos, rec = fileParser("tests_files/test_crearParejas.txt")
    par, rec["noObtuvo"] = crearParejas(pos)
    res = openFile("tests_files/resultado_crearParejas.txt", "r")
    lines = res.readlines()
    assert par == eval(lines[0])
    assert rec == eval(lines[1])
