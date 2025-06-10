import img2pdf
from PIL import Image # Necesario para verificar que el archivo es una imagen válida
import sys # Para manejar argumentos de línea de comandos y salir si hay errores

def convertir_imagen_simple_a_pdf(ruta_imagen, ruta_pdf_salida):
    """
    Convierte una sola imagen a un archivo PDF sin muchas comprobaciones adicionales.
    
    Args:
        ruta_imagen (str): Ruta del archivo de imagen de entrada.
        ruta_pdf_salida (str): Ruta donde se guardará el archivo PDF de salida.
    """
    try:
        # Intenta abrir la imagen con Pillow para verificar su validez básica
        # Esto lanzará un error si no es una imagen o está corrupta
        Image.open(ruta_imagen).verify() 
        
        # Convierte la imagen a PDF
        with open(ruta_pdf_salida, "wb") as f:
            f.write(img2pdf.convert(ruta_imagen))
        
        print(f"La imagen '{ruta_imagen}' ha sido convertida a '{ruta_pdf_salida}' exitosamente.")
        
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_imagen}' no fue encontrado.")
        sys.exit(1) # Sale del script con un código de error
    except Exception as e:
        print(f"Error al procesar la imagen o convertir a PDF: {e}")
        print("Asegúrate de que la ruta de la imagen es correcta y el archivo es una imagen válida.")
        sys.exit(1) # Sale del script con un código de error

# --- Uso del script desde la línea de comandos ---
if __name__ == "__main__":
    # Si ejecutas el script sin argumentos, te da una ayuda
    if len(sys.argv) < 3:
        print("Uso: python tu_script.py <ruta_de_imagen> <nombre_del_pdf_salida>")
        print("Ejemplo: python tu_script.py mi_foto.jpg salida.pdf")
        sys.exit(1) # Sale del script indicando que faltan argumentos

    # Los argumentos se obtienen de sys.argv:
    # sys.argv[0] es el nombre del script
    # sys.argv[1] es el primer argumento (la ruta de la imagen)
    # sys.argv[2] es el segundo argumento (la ruta del PDF de salida)
    imagen_entrada = sys.argv[1]
    pdf_salida = sys.argv[2]

    convertir_imagen_simple_a_pdf(imagen_entrada, pdf_salida)