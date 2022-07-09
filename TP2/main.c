#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <malloc.h>
#include <stdlib.h>

// Estructura utilizada para almacenar datos, para poder acceder a ellos de forma mas organizada.
typedef struct
{
    // Array que contiene todas la ciudades en orden, teniendo en cuenta su codigo postal.
    char **arrayCiudades;
    // Array que contiene la relacion de indice y genero.
    char arrayGenero[2];
    // Array que contiene la relacion de indice y gustos de genero.
    char arrayGustos[4];
} accesoDatos;

// Estructura utilizada para retornar mas valores de la funcion parserPersonas.
typedef struct
{
    // Array de array de chars, donde cada array de chars contiene la informacion de una persona.
    char **personas;
    // Largo de la array anterior que es equivalente a la cantidad de gente en los registros.
    long cantGente;
} infoPersonas;

// Funcion que se dedica a leer el archivo que contiene las ciudades y genera la anteriormente mencionada arrayCiudades.
char **parserCiudades(const char *fileName)
{
    char **arrayCiudades = NULL;
    FILE *fp;
    fp = fopen(fileName, "r");
    char buff[80];
    // Ciclo que recorre todos las lineas del archivo que contiene a las ciudades relacionadas con su codigo postal.
    for (int linea = 0; fgets(buff, 80, fp); linea++)
    {
        // Al ver que hay otra linea que contiene informacion de una ciudad, se pide memoria para poder almacenarla.
        arrayCiudades = (char **)realloc(arrayCiudades, (linea + 1) * sizeof(char *));
        // La string es almacenada como una array de chars, aca se reserva la memoria.
        char *temp = (char *)calloc(80, sizeof(char));
        int letraTemp = 0, letra = 0;

        // En esta porcion de codigo, se "parsea" el archivo para almacenar solo el nombre de la ciudad, ya que su codigo postal es el indice que la
        // ubica en la array.
        // Recorremos hasta encontrar una coma, que divide el codigo del nombre.
        while (buff[letra++] != ',')
            ;
        // Comenzamos a almacenar caracter a caracter en la ubicacion a la que apunta temp.
        while ((buff[letra] != ' ' || buff[letra + 1] != ' ') && (buff[letra] != '\n'))
        {
            temp[letraTemp] = buff[letra];
            letraTemp++;
            letra++;
        }
        // Finalizamos la nueva array con un caracter terminador.
        temp[letraTemp] = '\0';
        // Y hacemos que el puntero correspondiente apunte a temp.
        arrayCiudades[linea] = temp;
    }
    // Se cierra el archivo y se retorna la arrayCiudades.
    fclose(fp);
    return arrayCiudades;
}

// Funcion que se encarga de cargar el archivo que contiene las personas a una array, de arrays que contienen cada linea.
infoPersonas *parserPersonas(const char *fileName)
{
    // Se realliza un algoritmo parecido a la funcion anterior, pensamos en hacer una sola que cambie en la forma de parsear.
    // Pero decidimos hacer dos separadas para no aumentar la complejidad del codigo.
    infoPersonas *listaPersonas = (infoPersonas *)calloc(1, sizeof(infoPersonas));
    char **arrayPersonas = NULL;
    FILE *fp;
    fp = fopen(fileName, "r");
    char buff[80];
    int linea = 0;
    // Ciclo que recorre todas las lineas del archivo.
    while (fgets(buff, 80, fp))
    {
        arrayPersonas = (char **)realloc(arrayPersonas, (linea + 1) * sizeof(char *));
        char *temp = (char *)calloc(80, sizeof(char));
        // Copiamos en temp, el contenido de buff sin parsear. Ya que decidimos que es mas eficiente realizar
        // ese proceso solo con las personas seleccionadas de forma random.
        strcpy(temp, buff);
        arrayPersonas[linea] = temp;
        linea++;
    }
    fclose(fp);
    // Asignamos los valores a la estructura y la retornamos
    listaPersonas->personas = arrayPersonas;
    listaPersonas->cantGente = linea;
    return listaPersonas;
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
// para poder elegir de manera aleatoria las personas a conformar el archivo final.
// Genera numeros randoms por encima del necesario. Pero dado que la funcion rand, tiene un limite en cada computadora, decidimos utilizar esta
// funcion para ahorrar problemas.
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
// Modifica los valores necesarios de las personas y los escribe en el archivo de salida
// En vez de parsear la informacion de todas las personas, decidimos solo realizar este proceso con las personas seleccionadas
// para escribirse en el archivo, de esta forma en el peor de los casos se relaiza el parseo a todas las personas.
void escrituraSalida(char **partes, FILE *fp, accesoDatos *datos)
{
    // Lógica de modificacion de datos de las personas
    char *ptr;
    long index = strtol(partes[2], &ptr, 10);
    partes[2] = datos->arrayCiudades[--index];
    index = partes[4][0] - '0';
    partes[4][0] = datos->arrayGenero[--index];
    index = partes[5][0] - '0';
    partes[5][0] = datos->arrayGustos[--index];
    // Escritura al archivo de salida
    fputs(partes[0], fp);
    for (int indice = 1; indice < 4; indice++)
    {
        fputc(',', fp);
        fputs(partes[indice], fp);
    }
    for (int indice = 4; indice < 6; indice++)
    {
        fputc(',', fp);
        fputc(partes[indice][0], fp);
    }
    fputc('\n', fp);
}

// Funcoin que se encarga de escribir el archivo salida.
void escritorDeArchivo(long cantGenteP, infoPersonas *listaPersonas, const char *fileName, accesoDatos *datos)
{
    if(cantGenteP > listaPersonas->cantGente)
        printf("%s", "La cantidad de gente pedida exede la cantidad registrada, no se puede ejecutar.");
    else{
        FILE *fp;
        // Abrimios un archivo en modo escritura, sino existe se creara.
        fp = fopen(fileName, "w");
        // Calculamos de forma aleatoria las personas.
        long *listRand = calcRand(listaPersonas->cantGente);
        // Recorremos la lista de indeces de personas aleatorias, mientras seran escritas en el archivo.
        for (long i = 0; i < cantGenteP; i++)
        {
            // Asigno memoria para el array que va a contener cada dato de la persona
            char **partes;
            partes = (char **)calloc(6, sizeof(char *));
            char *parte;
            // Mediante strtok separamos la entrada mediante las comas
            parte = strtok(listaPersonas->personas[listRand[i]], ",");
            for (int indice = 0; parte != NULL; indice++)
            {
                partes[indice] = parte;
                parte = strtok(NULL, ",");
            }
            // Aplicamos la logica correspondiente a cada parte de la entrada
            // y escribimos el resultado en el archivo de salida "salida.txt"
            escrituraSalida(partes, fp, datos);
            // Liberamos la memoria
            free(partes);
        }
        // Cerramos el archivo de salida
        fclose(fp);
    }
}

int main()
{
    // Creamos la estructura de datos a modificar de las peronas (localidad, genero y genero de interes)
    accesoDatos datos;
    datos.arrayCiudades = parserCiudades("codigoLocalidades.txt");
    strcpy(datos.arrayGenero, "MF");
    strcpy(datos.arrayGustos, "FMAN");
    // Creamos la estructura con las personas y su cantidad
    infoPersonas *listaPersonas = parserPersonas("personas.txt");
    // Ingreso por teclado de la cantidad de personas a seleccionar para modificar y escribir como salida
    long cantGenteP;
    printf("%s", "Ingresa la cantidad de personas a parsear: ");
    scanf("%ld", &cantGenteP);
    // Llamamos a la funcion que se encarga de procesar las personas y escribirlas en el archivo de salida
    escritorDeArchivo(cantGenteP, listaPersonas, "salida.txt", &datos);
    return 0;
}
