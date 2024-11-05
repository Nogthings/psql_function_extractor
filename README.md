SQL Function Extractor
Este programa toma un archivo CSV con funciones almacenadas y genera archivos .sql independientes, donde el nombre de cada archivo es el valor de la primera columna (proname) y el contenido es el valor de la segunda columna (prosrc), permitiendo una organización fácil de funciones SQL exportadas.

Tabla de Contenidos
Requisitos
Instalación
Uso
Obtener el archivo CSV
Ejecutar el programa
Opcional: Crear un ejecutable
Ejemplo de Uso
Notas
Requisitos
Python 3.6 o superior
Biblioteca gráfica tkinter (ya viene instalada por defecto con Python en la mayoría de sistemas)
Acceso a una base de datos PostgreSQL para realizar la consulta y generar el archivo CSV
Instalación
Clona este repositorio o descarga el archivo del script:
bash
Copy code
git clone <URL-del-repositorio>
cd sql_function_extractor
Instala las dependencias necesarias (si el programa requiere alguna):
bash
Copy code
pip install -r requirements.txt
Nota: Asegúrate de tener tkinter y PyInstaller instalados si deseas crear un ejecutable.

Uso
Obtener el archivo CSV
Abre tu cliente de PostgreSQL y ejecuta la siguiente consulta para obtener el archivo CSV. Esta consulta extrae el nombre de la función (proname) y el código de la función (prosrc) de todas las funciones en la base de datos que contienen el término 'procedimientos_a_buscar'.

sql
Copy code
\copy (SELECT proname, prosrc FROM pg_proc WHERE prosrc LIKE '%procedimientos_a_buscar%') TO 'functions.csv' CSV HEADER;
Esto generará un archivo functions.csv en el directorio actual, con las columnas proname y prosrc.
Guarda el archivo CSV en la misma carpeta que el programa o en otra ubicación conocida.

Ejecutar el programa
Desde el terminal o consola, ejecuta el programa de la siguiente manera:

bash
Copy code
python index.py
Aparecerá una ventana gráfica en la que podrás seleccionar el archivo CSV (usando el botón de selección de archivo) y la carpeta de destino donde se generarán los archivos .sql.

Cada archivo generado llevará como nombre el valor de la columna proname y su contenido será el valor de la columna prosrc.

Opcional: Crear un ejecutable
Si deseas crear un ejecutable para simplificar el uso del programa, puedes hacerlo con PyInstaller:

bash
Copy code
pyinstaller --onefile --windowed index.py
Este comando generará un archivo ejecutable en la carpeta dist. Podrás ejecutarlo directamente sin necesidad de tener Python instalado.

Ejemplo de Uso
Genera el archivo CSV:

sql
Copy code
\copy (SELECT proname, prosrc FROM pg_proc WHERE prosrc LIKE '%procedimientos_a_buscar%') TO 'functions.csv' CSV HEADER;
Ejecuta el programa:

bash
Copy code
python index.py
Selecciona functions.csv y la carpeta de destino en la interfaz gráfica.

Una vez completado, en la carpeta de destino encontrarás archivos .sql con el nombre y contenido de cada función encontrada en el archivo CSV.

Notas
Si encuentras algún problema, asegúrate de que el archivo CSV tenga las columnas proname y prosrc en el orden correcto.
El programa crea un archivo .sql independiente por cada fila en el CSV. Verifica la carpeta de destino para confirmar que los archivos se generaron correctamente.