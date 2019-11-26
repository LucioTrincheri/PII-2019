def parserArchivo(pathF):
    file = open(pathF, 'r')
    maze = []
    lines = file.readlines()
    for line in lines:
        print(line)
        line = line.strip('\n').strip('\r')
        maze.append([int(digit) for digit in line])
    file.close()
    return maze


laberinto = parserArchivo("test_files/test_mazeParser.txt")
print(laberinto)
