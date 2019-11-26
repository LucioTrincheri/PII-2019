#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <malloc.h>
#include <stdlib.h>

// Estructura donde se guarda todo la informacion del laberinto
typedef struct
{
  // Numero de paredes a ubicar de forma random,
  // Numero de paredes definidas por la entrada y
  // Longitud del laberinto respectivamente
  int nParRan, nParDef, dimen;
  // Fila y columna tanto de la posicion de inicio como de la final
  int posInicio[2], posFin[2];
  // Lista de posiciones de paredes a escribir en el archivo de salida
  int **listaPosParedes;
} Laberinto;

// Funcion que lee el archivo de entrada y procesa la informacion,
// la cual sera utilizada para escribir el archivo de salida
Laberinto *parserEntrada(char *fileName)
{
  // Abro el archivo de entrada en forma de lectura
  FILE *fp;
  fp = fopen(fileName, "r");
  // Asigno memoria a la estructura
  Laberinto *datos = calloc(1, sizeof(Laberinto));
  datos->listaPosParedes = NULL;
  // Variables auxiliares
  int seccion = 0;
  int numeroPared = 0;
  char buff[40];
  // Recorro el archivo hasta el final, escribiendo en la
  // estructura la informacion segun el esquema de entrada
  while (fgets(buff, 40, fp))
  {
    // Longitud del laberinto
    if (seccion == 1)
    {
      datos->dimen = buff[0] - '0';
      seccion++;
    }
    // Cantidad de paredes random
    if (seccion == 4)
    {
      datos->nParRan = buff[0] - '0';
      seccion++;
    }
    // Coordenadas...
    if (buff[0] == '(')
    {
      // ...de las paredes definidas
      if (seccion == 3)
      {
        datos->listaPosParedes = (int **)realloc(datos->listaPosParedes, sizeof(int *) * (numeroPared + 1));
        datos->listaParedes[numeroPared] = (int *)malloc(sizeof(int) * 2);
        datos->listaParedes[numeroPared][0] = buff[1] - '0';
        datos->listaParedes[numeroPared][1] = buff[3] - '0';
        numeroPared++;
      }
      else
      {
        // ...de la posicion de inicio
        if (seccion == 6)
        {
          datos->posInicio[0] = buff[1] - '0';
          datos->posInicio[1] = buff[3] - '0';
        }
        // ...de la posicion objetivo
        else
        {
          datos->posFin[0] = buff[1] - '0';
          datos->posFin[1] = buff[3] - '0';
        }
      }
    }
    // Aumento la seccion en la que me encuentro
    if (buff[0] == 'o' || buff[0] == 'p' || buff[0] == 'd')
    {
      seccion++;
    }
  }
  // Guardo el numero de paredes definidas
  datos->nParDef = indiceParedes;
  // Cierro el archivo y retorno los datos
  fclose(fp);
  return datos;
}

// TODO -> Funcion de escritura del archivo de salida

int main()
{
  // TODO -> Entrada del archivo por teclado
  Laberinto *datos = parserEntrada("entrada.txt");
  return 0;
}