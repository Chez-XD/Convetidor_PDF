import img2pdf
from PIL import Image # Necesario para verificar que el archivo es una imagen válida
import sys # Para manejar argumentos de línea de comandos y salir si hay errores
import os # Para listar el contenido de directorios y construir rutas

def convertir_imagenes_a_pdf(ruta_carpeta_imagenes, ruta_pdf_salida):
    """
    Convierte todas las imágenes encontradas en una carpeta a un único archivo PDF.

    Args:
        ruta_carpeta_imagenes (str): Ruta de la carpeta que contiene las imágenes.
        ruta_pdf_salida (str): Ruta donde se guardará el archivo PDF de salida.
    """
    imagenes_a_convertir = []
    extensiones_imagen_validas = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    # 1. Verificar si la carpeta de entrada existe
    if not os.path.isdir(ruta_carpeta_imagenes):
        print(f"Error: La carpeta '{ruta_carpeta_imagenes}' no fue encontrada o no es un directorio.")
        sys.exit(1)

    # 2. Recorrer la carpeta y recolectar las rutas de las imágenes
    print(f"Buscando imágenes en: '{ruta_carpeta_imagenes}'...")
    for nombre_archivo in os.listdir(ruta_carpeta_imagenes):
        # Construir la ruta completa del archivo
        ruta_completa_archivo = os.path.join(ruta_carpeta_imagenes, nombre_archivo)

        # Asegurarse de que es un archivo (no un subdirectorio) y que tiene una extensión de imagen válida
        if os.path.isfile(ruta_completa_archivo) and nombre_archivo.lower().endswith(extensiones_imagen_validas):
            try:
                # Opcional: Intentar abrir la imagen con Pillow para una verificación básica de validez
                # Esto es útil para evitar errores de img2pdf con archivos corruptos o no válidos
                Image.open(ruta_completa_archivo).verify()
                imagenes_a_convertir.append(ruta_completa_archivo)
                print(f"  - Encontrada: {nombre_archivo}")
            except Exception as e:
                print(f"  - Advertencia: '{nombre_archivo}' parece no ser una imagen válida o está corrupta. Ignorando. ({e})")
        else:
            print(f"  - Ignorando: {nombre_archivo} (no es un archivo de imagen válido o es una carpeta)")

    if not imagenes_a_convertir:
        print(f"No se encontraron imágenes válidas en la carpeta '{ruta_carpeta_imagenes}'.")
        sys.exit(1)

    # Opcional: Ordenar las imágenes por nombre para asegurar un orden consistente en el PDF
    imagenes_a_convertir.sort()
    print(f"\nSe encontraron {len(imagenes_a_convertir)} imágenes válidas para convertir.")

    # 3. Realizar la conversión a PDF
    try:
        with open(ruta_pdf_salida, "wb") as f:
            f.write(img2pdf.convert(imagenes_a_convertir)) # img2pdf.convert ahora recibe una lista de rutas
        
        print(f"\nTodas las imágenes de '{ruta_carpeta_imagenes}' han sido convertidas a '{ruta_pdf_salida}' exitosamente.")
        
    except Exception as e:
        print(f"\nError al convertir las imágenes a PDF: {e}")
        print("Asegúrate de que las imágenes son válidas y tienes permisos de escritura en la ruta de salida.")
        sys.exit(1)

# --- Uso del script desde la línea de comandos ---
if __name__ == "__main__":
    # Ahora el script espera la ruta de la carpeta y el nombre del PDF
    if len(sys.argv) < 3:
        print("Uso: python tu_script.py <ruta_de_carpeta_de_imagenes> <nombre_del_pdf_salida>")
        print("Ejemplo: python tu_script.py /home/chez/mis_fotos_vacaciones informe_final.pdf")
        print("\nNota: Asegúrate de que las rutas son correctas y de que el entorno virtual esté activo.")
        sys.exit(1)

    carpeta_imagenes_entrada = sys.argv[1]
    pdf_salida = sys.argv[2]

    convertir_imagenes_a_pdf(carpeta_imagenes_entrada, pdf_salida)
    