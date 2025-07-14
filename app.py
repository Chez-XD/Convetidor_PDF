from flask import Flask, render_template, request, send_file, jsonify
import os
import sys
import uuid # Para generar nombres únicos para archivos temporales

# Importar tu función de conversión desde el script de conversión
# Asegúrate de que el nombre del archivo coincida (convertidor_PDF o convertidor_multiple_pdf)
try:
    from convertidor_PDF import convertir_imagenes_a_pdf
except ImportError:
    # Esto es solo para depuración si hay problemas de importación con Flask
    print("Error: No se pudo importar 'convertir_imagenes_a_pdf'.")
    sys.exit(1)

app = Flask(__name__)

# Directorio donde se guardarán temporalmente las imágenes subidas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Directorio donde se guardarán temporalmente los PDFs generados
OUTPUT_FOLDER = 'pdfs_generados'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    # Sirve el archivo HTML principal cuando accedes a la raíz del servidor
    return render_template('index.html')

@app.route('/convertir', methods=['POST'])
def convertir():
    if 'files' not in request.files:
        return jsonify({"success": False, "message": "No se encontraron archivos."}), 400

    uploaded_files = request.files.getlist('files')
    pdf_name = request.form.get('pdfName', 'documento_generado.pdf')

    if not uploaded_files:
        return jsonify({"success": False, "message": "No se seleccionaron archivos."}), 400
    
    if not pdf_name:
        pdf_name = 'documento_generado.pdf' # Nombre por defecto si no se proporciona

    # Asegurarse de que el nombre del PDF termine en .pdf
    if not pdf_name.lower().endswith(".pdf"):
        pdf_name += ".pdf"

    # Crear un directorio temporal único para cada lote de imágenes subidas
    session_id = str(uuid.uuid4())
    temp_input_dir = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(temp_input_dir, exist_ok=True)

    image_paths = []
    for file in uploaded_files:
        if file.filename == '':
            continue
        # Asegurarse de que solo se guarden archivos de imagen permitidos
        # (Aquí puedes añadir más validación si quieres)
        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            filepath = os.path.join(temp_input_dir, file.filename)
            file.save(filepath)
            image_paths.append(filepath)

    if not image_paths:
        # Limpiar directorio temporal si no se guardaron imágenes válidas
        os.rmdir(temp_input_dir)
        return jsonify({"success": False, "message": "No se encontraron imágenes válidas para procesar."}), 400

    # Ruta de salida del PDF en el servidor
    output_pdf_path = os.path.join(OUTPUT_FOLDER, pdf_name)

    try:
        # Llama a tu función de conversión de imágenes a PDF
        convertir_imagenes_a_pdf(temp_input_dir, output_pdf_path)

        # Limpiar el directorio temporal de las imágenes subidas después de la conversión
        for img_path in image_paths:
            os.remove(img_path)
        os.rmdir(temp_input_dir)

        # Envía el PDF al cliente para su descarga
        # 'as_attachment=True' fuerza la descarga en lugar de abrirlo en el navegador
        # 'mimetype' es importante para que el navegador sepa que es un PDF
        return send_file(output_pdf_path, as_attachment=True, mimetype='application/pdf', download_name=pdf_name)

    except Exception as e:
        # Limpiar el directorio temporal en caso de error
        for img_path in image_paths:
            if os.path.exists(img_path): # Asegurarse de que exista antes de intentar eliminar
                os.remove(img_path)
        if os.path.exists(temp_input_dir):
            os.rmdir(temp_input_dir)
        
        # También limpiar el PDF si se creó parcialmente antes del error
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)

        return jsonify({"success": False, "message": f"Error durante la conversión: {str(e)}"}), 500

if __name__ == '__main__':
    # Ejecuta el servidor Flask en modo de depuración (útil para desarrollo)
    app.run(debug=True)