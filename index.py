import sys
import csv
import os
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox, QHeaderView, QMessageBox

class FunctionExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extractor de Funciones")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Botón para seleccionar archivo
        self.select_file_button = QPushButton("Seleccionar CSV")
        self.select_file_button.clicked.connect(self.select_csv_file)
        layout.addWidget(self.select_file_button)

        # Botón para limpiar la carga de funciones
        self.clear_table_button = QPushButton("Limpiar Carga")
        self.clear_table_button.clicked.connect(self.clear_table)
        layout.addWidget(self.clear_table_button)

        # Checkbox para seleccionar/deseleccionar todo
        self.select_all_checkbox = QCheckBox("Seleccionar Todo")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        layout.addWidget(self.select_all_checkbox)

        # Tabla para mostrar las funciones y checkboxes
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  # Dos columnas: una para el nombre de la función, otra para el checkbox
        self.table.setHorizontalHeaderLabels(["Nombre de la Funcion", "Exportar"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Botón para generar los archivos SQL
        self.generate_button = QPushButton("Generar Archivos SQL")
        self.generate_button.clicked.connect(self.generate_sql_files)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def select_csv_file(self):
        options = QFileDialog.Options()
        csv_file, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "CSV Files (*.csv)", options=options)
        if csv_file:
            self.load_csv_data(csv_file)

    def load_csv_data(self, csv_file):
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.table.setRowCount(0)  # Limpiar la tabla

                # Llenar la tabla con los datos del CSV
                for row in reader:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Nombre de la función en la primera columna
                    self.table.setItem(row_position, 0, QTableWidgetItem(row['proname']))

                    # Checkbox en la segunda columna
                    check_box_item = QCheckBox()
                    check_box_item.setChecked(True)  # Por defecto, todos los checkboxes están seleccionados
                    self.table.setCellWidget(row_position, 1, check_box_item)

                # Restablecer el estado de select_all_checkbox
                self.select_all_checkbox.setChecked(True)

        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")

    def clear_table(self):
        """Limpia la tabla y restablece el checkbox de selección de todo."""
        self.table.setRowCount(0)
        self.select_all_checkbox.setChecked(False)

    def toggle_select_all(self):
        """Selecciona o deselecciona todos los checkboxes en la tabla."""
        select_all = self.select_all_checkbox.isChecked()
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 1)
            checkbox.setChecked(select_all)

    def generate_sql_files(self):
        # Pedir al usuario que seleccione la carpeta de destino
        output_dir = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino")
        if not output_dir:
            QMessageBox.warning(self, "Sin carpeta seleccionada", "No se seleccionó ninguna carpeta de destino.")
            return

        # Contador de archivos generados
        generated_count = 0

        # Generar un archivo SQL para cada función seleccionada
        for row in range(self.table.rowCount()):
            function_name_item = self.table.item(row, 0)
            checkbox = self.table.cellWidget(row, 1)

            if checkbox.isChecked():
                function_name = function_name_item.text()

                # Generar un nombre de archivo único
                file_path = self.get_unique_file_path(output_dir, function_name)

                # Contenido de ejemplo para el archivo SQL
                sql_content = f"-- SQL script for function: {function_name}\nCREATE OR REPLACE FUNCTION {function_name}() RETURNS void AS $$\nBEGIN\n    -- Function logic here\nEND;\n$$ LANGUAGE plpgsql;"

                # Escribir el archivo SQL
                try:
                    with open(file_path, 'w') as file:
                        file.write(sql_content)
                    generated_count += 1
                except Exception as e:
                    print(f"Error al escribir el archivo {file_path}: {e}")
                    QMessageBox.critical(self, "Error", f"Error al escribir el archivo {file_path}: {e}")

        # Mostrar mensaje de confirmación con botón para abrir la carpeta
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Archivos generados")
        msg_box.setText(f"Se generaron {generated_count} archivos SQL en la carpeta seleccionada.")
        open_folder_button = msg_box.addButton("Abrir carpeta", QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Ok)
        open_folder_button.setFocus()  # Establece el enfoque en el botón "Abrir carpeta"

        msg_box.exec_()

        # Abrir la carpeta si el usuario presiona "Abrir carpeta"
        if msg_box.clickedButton() == open_folder_button:
            self.open_folder(output_dir)

        # Reiniciar la aplicación después de la generación
        self.clear_table()

    def get_unique_file_path(self, directory, base_name):
        """Genera un nombre de archivo único en el directorio dado."""
        file_path = os.path.join(directory, f"{base_name}.sql")
        counter = 1
        # Agrega un sufijo numérico si el archivo ya existe
        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name}_{counter}.sql")
            counter += 1
        return file_path

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{path}'")
        else:  # Linux
            os.system(f"xdg-open '{path}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionExtractorApp()
    window.show()
    sys.exit(app.exec_())
