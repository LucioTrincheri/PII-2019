#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <malloc.h>
#include <stdlib.h>
#include <time.h>

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
  int **listaPosParedesDefinidas;
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
  datos->listaPosParedesDefinidas = NULL;
  // Variables auxiliares
  int seccion = 0;
  int numeroPared = 0;
  char buff[40];
  // Recorro el archivo hasta el final, escribiendo en la
  // estructura la informacion segun el esquema de entrada
  while (fgets(buff, 40, fp))
  {
    char *ptr;
    // Longitud del laberinto
    if (seccion == 1)
    {
      sscanf(buff, "%d", &(datos->dimen));
      seccion++;
    }
    // Cantidad de paredes random
    if (seccion == 4)
    {
      sscanf(buff, "%d", &(datos->nParRan));
      seccion++;
    }
    // Coordenadas...
    if (buff[0] == '(')
    {
      // ...de las paredes definidas
      if (seccion == 3 && !(buff[0] == 'o' || buff[0] == 'p' || buff[0] == 'd'))
      {
        datos->listaPosParedesDefinidas = (int **)realloc(datos->listaPosParedesDefinidas, sizeof(int *) * (numeroPared + 1));
        datos->listaPosParedesDefinidas[numeroPared] = (int *)malloc(sizeof(int) * 2);
        sscanf(buff, "(%[^)\n]", buff);
        datos->listaPosParedesDefinidas[numeroPared][0] = strtol(strtok(buff, ","), &ptr, 10) - 1;
        datos->listaPosParedesDefinidas[numeroPared][1] = strtol(strtok(NULL, ","), &ptr, 10) - 1;
        numeroPared++;
      }
      else
      {
        // ...de la posicion de inicio
        if (seccion == 6)
        {
          // TODO IMPORTANTE cambiar los buff por su strtok correspondiente
          sscanf(buff, "(%[^)\n]", buff);
          datos->posInicio[0] = strtol(strtok(buff, ","), &ptr, 10) - 1;
          datos->posInicio[1] = strtol(strtok(NULL, ","), &ptr, 10) - 1;
        }
        // ...de la posicion objetivo
        else
        {
          sscanf(buff, "(%[^)\n]", buff);
          datos->posFin[0] = strtol(strtok(buff, ","), &ptr, 10) - 1;
          datos->posFin[1] = strtol(strtok(NULL, ","), &ptr, 10) - 1;
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
  datos->nParDef = numeroPared;
  // Cierro el archivo y retorno los datos
  fclose(fp);
  return datos;
}

// Funcion auxiliar, que realiza un intercambio del contenido de dos variables.
void swap(long *a, long *b)
{
  // Utilizamos variables en modo long ya que esta funcion es utilizada en otra funcion que obtiene de manera aleatoria los indices de las personas
  // en la arrayPersona
  long c;
  c = *a;
  *a = *b;
  *b = c;
}

// Funcion que devulve una array de numeros unicos, generados de manera random,
// los cuales seran usados de indice para agarrar las posiciones
// que seran asignadas como paredes random.
long *calcRand(long cantGente)
{
  // Introduciomos la generacion de numeros aleatorios.
  srand(time(NULL));
  // Se reserva arrayPersonasmemoria para la variable resultado que sera una array de longs.
  long *resultado = (long *)calloc(cantGente, sizeof(long));
  // Se rellena una array de largo de la cantidad de gente pedidad de forma acendiente.
  for (long i = 0; i < cantGente; i++)
  {
    resultado[i] = i;
  }
  // Cilio que randomiza los resultados, intercambiando los contenidos de cada posicion de la array.
  for (long i = cantGente - 1; i >= 0; i--)
  {
    unsigned long x = rand();
    x <<= 15;
    x ^= rand();
    x %= cantGente;
    swap(&(resultado[i]), &(resultado[x]));
  }
  return resultado;
}

// Con la informacion parseada, creo el laberinto y lo escribo en el archivo de salida
void escrituraSalida(Laberinto *datos)
{
  // Laberinto final a escribir
  char laberinto[datos->dimen][datos->dimen];
  // Escribo todo el laberinto como 0 en un principio
  for (int i = 0; i < datos->dimen; i++)
  {
    for (int j = 0; j < datos->dimen; j++)
    {
      laberinto[i][j] = '0';
    }
  }
  // Escribo la posicion de salida y de fin
  laberinto[datos->posInicio[0]][datos->posInicio[1]] = 'I';
  laberinto[datos->posFin[0]][datos->posFin[1]] = 'X';
  // Escribo las paredes definidas
  for (int i = 0; i < datos->nParDef; i++)
  {
    laberinto[datos->listaPosParedesDefinidas[i][0]][datos->listaPosParedesDefinidas[i][1]] = '1';
  }
  // Hago un array de los valores que pueden ser posibles paredes random
  int **arrayDeCeros = NULL;
  int numeroDeCeros = 0;
  for (int i = 0; i < datos->dimen; i++)
  {
    for (int j = 0; j < datos->dimen; j++)
    {
      if (laberinto[i][j] == '0')
      {
        // Por cada cero que encuentro, guardo su posicion en el array
        arrayDeCeros = (int **)realloc(arrayDeCeros, sizeof(int *) * (numeroDeCeros + 1));
        arrayDeCeros[numeroDeCeros] = (int *)malloc(sizeof(int) * 2);
        arrayDeCeros[numeroDeCeros][0] = i;
        arrayDeCeros[numeroDeCeros][1] = j;
        numeroDeCeros++;
      }
    }
  }
  // Genero una lista de valores random que sera usada como indice
  long *listRand = calcRand(numeroDeCeros);
  // Transformo los primeros nParRan numeros, usando a listRand como indice
  for (int i = 0; i < datos->nParRan; i++)
  {
    int aux = listRand[i];
    laberinto[arrayDeCeros[aux][0]][arrayDeCeros[aux][1]] = '1';
  }

  // Escritura de archivo
  FILE *fp = fopen("laberinto.txt", "w");
  for (int i = 0; i < datos->dimen; i++)
  {
    for (int j = 0; j < datos->dimen; j++)
    {
      fputc(laberinto[i][j], fp);
    }
    fputc('\n', fp);
  }
  // Cierro el archivo
  fclose(fp);
  // Liberar memoria
  free(listRand);
  free(arrayDeCeros);
}

int main(int argc, char *argv[])
{
  Laberinto *datos = parserEntrada(argv[1]);
  escrituraSalida(datos);
  for (int i = 0; i < datos->nParDef; i++)
  {
    free(datos->listaPosParedesDefinidas[i]);
  }
  free(datos->listaPosParedesDefinidas);
  free(datos);
  return 0;
}