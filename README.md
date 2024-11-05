# SQL Function Extractor

Este programa toma un archivo CSV con funciones almacenadas y genera archivos `.sql` independientes, donde el nombre de cada archivo es el valor de la primera columna (`proname`) y el contenido es el valor de la segunda columna (`prosrc`), permitiendo una organización fácil de funciones SQL exportadas.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
  - [Obtener el archivo CSV](#obtener-el-archivo-csv)
  - [Ejecutar el programa](#ejecutar-el-programa)
- [Opcional: Crear un ejecutable](#opcional-crear-un-ejecutable)
- [Ejemplo de Uso](#ejemplo-de-uso)
- [Notas](#notas)

## Requisitos

- **Python 3.6 o superior**
- **Biblioteca gráfica** `tkinter` *(ya viene instalada por defecto con Python en la mayoría de sistemas)*
- **Acceso a una base de datos PostgreSQL** para realizar la consulta y generar el archivo CSV

## Instalación

1. Clona este repositorio o descarga el archivo del script:
   ```bash
   git clone <URL-del-repositorio>
   cd sql_function_extractor


## Ejemplo de Uso

1. Genera el archivo CSV ejecutando la siguiente consulta en tu cliente de PostgreSQL:

   ```sql
   \copy (SELECT proname, prosrc FROM pg_proc WHERE prosrc LIKE '%procedimientos_a_buscar%') TO 'functions.csv' CSV HEADER;
