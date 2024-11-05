import csv
import os
from tkinter import filedialog, messagebox, Tk, Label, Entry, Button

def csv_to_individual_sql_files(csv_file, output_dir):
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Verificamos que el archivo CSV tenga las columnas necesarias
            if 'proname' not in reader.fieldnames or 'prosrc' not in reader.fieldnames:
                messagebox.showerror("Error", "El archivo CSV no contiene las columnas 'proname' y 'prosrc'")
                return
            
            # Creamos la carpeta de salida si no existe
            os.makedirs(output_dir, exist_ok=True)
            
            # Iteramos sobre cada fila y creamos un archivo independiente
            for row in reader:
                proname = row['proname']
                prosrc = row['prosrc']

                # Cambiamos comillas simples para evitar errores en el contenido SQL
                prosrc = prosrc.replace("'", "''")

                # Generamos el nombre del archivo .sql y su contenido
                sql_file_path = os.path.join(output_dir, f"{proname}.sql")
                with open(sql_file_path, 'w', encoding='utf-8') as sqlfile:
                    sqlfile.write(f"-- SQL script for {proname}\n")
                    sqlfile.write(f"CREATE OR REPLACE FUNCTION {proname}() RETURNS void AS $$\n{prosrc}\n$$ LANGUAGE plpgsql;\n")

        messagebox.showinfo("Éxito", f"Archivos .sql generados exitosamente en '{output_dir}'")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def select_csv_file():
    csv_file_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV Files", "*.csv")])
    if csv_file_path:
        csv_entry.delete(0, 'end')
        csv_entry.insert(0, csv_file_path)

def select_output_directory():
    output_dir_path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
    if output_dir_path:
        output_entry.delete(0, 'end')
        output_entry.insert(0, output_dir_path)

def generate_sql_files():
    csv_file = csv_entry.get()
    output_dir = output_entry.get()
    if not csv_file or not output_dir:
        messagebox.showerror("Error", "Por favor selecciona el archivo CSV y la carpeta de salida.")
        return
    csv_to_individual_sql_files(csv_file, output_dir)

# Configuración de la interfaz gráfica
root = Tk()
root.title("Extractor de funciones postgres")
root.geometry("800x300")

Label(root, text="Archivo CSV:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
csv_entry = Entry(root, width=50)
csv_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Seleccionar...", command=select_csv_file).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Carpeta de salida:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_entry = Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Seleccionar...", command=select_output_directory).grid(row=1, column=2, padx=10, pady=10)

Button(root, text="Generar Archivos SQL", command=generate_sql_files, bg="lightblue").grid(row=2, column=1, pady=20)

root.mainloop()
