import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext # Importamos módulos necesarios para GUI
import os
import sys

# Importar tus funciones de conversión
# Asegúrate de que este script esté en el mismo directorio que tu convertidor_multiple_pdf.py
# O ajusta la ruta de importación si está en otro lugars
try:
    # Intentamos importar la función del otro script.
    # Si cambiaste el nombre del script principal, ajusta 'convertidor_multiple_pdf'
    from convertidor_PDF import convertir_imagenes_a_pdf
except ImportError:
    # Si no se encuentra el script, mostramos un error y salimos
    messagebox.showerror("Error de Importación", "No se pudo importar 'convertir_imagenes_a_pdf'. Asegúrate de que 'convertidor_multiple_pdf.py' esté en el mismo directorio o que la ruta sea correcta.")
    sys.exit(1)

class PDFConverterApp:
    def __init__(self, master):
        self.master = master # La ventana principal
        master.title("Convertidor de Imágenes a PDF") # Título de la ventana
        master.geometry("600x450") # Tamaño inicial de la ventana

        # Variables de Tkinter para almacenar y mostrar datos
        self.input_folder_path = tk.StringVar() # Para la ruta de la carpeta de imágenes
        self.output_pdf_name = tk.StringVar() # Para el nombre del PDF de salida
        self.output_pdf_name.set("documento_final.pdf") # Nombre por defecto para el PDF

        # --- Widgets de la Interfaz ---

        # 1. Marco para la selección de la carpeta de imágenes de entrada
        frame_input = tk.LabelFrame(master, text="Carpeta de Imágenes de Entrada")
        frame_input.pack(pady=10, padx=10, fill="x", expand=True)

        self.entry_input_folder = tk.Entry(frame_input, textvariable=self.input_folder_path, width=50)
        self.entry_input_folder.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.btn_browse_input = tk.Button(frame_input, text="Seleccionar Carpeta", command=self.browse_input_folder)
        self.btn_browse_input.pack(side="right", padx=5, pady=5)

        # 2. Marco para el nombre del archivo PDF de salida
        frame_output = tk.LabelFrame(master, text="Nombre del Archivo PDF de Salida")
        frame_output.pack(pady=10, padx=10, fill="x", expand=True)

        self.entry_output_pdf = tk.Entry(frame_output, textvariable=self.output_pdf_name, width=50)
        self.entry_output_pdf.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # 3. Botón para iniciar la conversión
        self.btn_convert = tk.Button(master, text="Convertir a PDF", command=self.convert_images)
        self.btn_convert.pack(pady=15)

        # 4. Área de texto con scroll para mostrar mensajes (log)
        self.log_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=10)
        self.log_text.pack(pady=10, padx=10, fill="both", expand=True)
        self.log_message("Aplicación iniciada. Selecciona una carpeta de imágenes y un nombre para el PDF.")

    def browse_input_folder(self):
        """Abre un diálogo para seleccionar la carpeta de imágenes."""
        folder_selected = filedialog.askdirectory() # Abre la ventana para seleccionar directorio
        if folder_selected: # Si el usuario seleccionó una carpeta
            self.input_folder_path.set(folder_selected) # Actualiza la variable de Tkinter
            self.log_message(f"Carpeta seleccionada: {folder_selected}")

    def log_message(self, message):
        """Inserta un mensaje en el área de log de la GUI."""
        self.log_text.insert(tk.END, message + "\n") # Añade el mensaje al final
        self.log_text.see(tk.END) # Asegura que el área de texto se desplace al final

    def convert_images(self):
        """Función que se llama al presionar el botón 'Convertir a PDF'."""
        input_folder = self.input_folder_path.get() # Obtiene la ruta de la carpeta
        output_pdf = self.output_pdf_name.get() # Obtiene el nombre del PDF

        # Validaciones básicas
        if not input_folder:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta de imágenes.")
            return
        if not output_pdf:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre para el archivo PDF de salida.")
            return
        
        # Construye la ruta completa del PDF de salida
        # Por simplicidad, el PDF se guardará en la misma carpeta de las imágenes
        output_pdf_full_path = os.path.join(input_folder, output_pdf)
        
        # Asegúrate de que el nombre del PDF termine en .pdf
        if not output_pdf_full_path.lower().endswith(".pdf"):
            output_pdf_full_path += ".pdf"

        self.log_message(f"\nIniciando conversión...")
        self.log_message(f"Carpeta de entrada: {input_folder}")
        self.log_message(f"PDF de salida: {output_pdf_full_path}")

        try:
            # Redirigimos sys.stdout temporalmente para capturar los mensajes de print de tu script
            # y mostrarlos en el área de log de la GUI.
            old_stdout = sys.stdout # Guardamos la salida estándar original
            sys.stdout = TextRedirector(self.log_text) # Redirigimos a nuestra clase

            # Aquí llamamos a tu función de conversión original
            convertir_imagenes_a_pdf(input_folder, output_pdf_full_path)
            
            sys.stdout = old_stdout # Restauramos la salida estándar
            self.log_message("\n¡Conversión completada exitosamente!")
            messagebox.showinfo("Éxito", f"El PDF '{output_pdf}' ha sido creado en '{input_folder}'.")

        except Exception as e:
            sys.stdout = old_stdout # Asegurarse de restaurar stdout incluso si hay error
            self.log_message(f"\n¡Error durante la conversión: {e}")
            messagebox.showerror("Error de Conversión", f"Ocurrió un error: {e}")

# Clase auxiliar para redirigir la salida de `print()` a nuestro widget `ScrolledText`
class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str_to_write):
        self.widget.insert(tk.END, str_to_write)
        self.widget.see(tk.END) # Auto-scroll para ver los mensajes nuevos

    def flush(self):
        # Este método es necesario para la compatibilidad con sys.stdout, pero no hace nada aquí.
        pass

# --- Ejecutar la Aplicación ---
if __name__ == "__main__":
    root = tk.Tk() # Crea la ventana principal de Tkinter
    app = PDFConverterApp(root) # Crea una instancia de nuestra aplicación
    root.mainloop() # Inicia el bucle principal de la GUI para que la ventana se mantenga abierta