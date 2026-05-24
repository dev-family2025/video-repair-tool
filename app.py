import os
import ffmpeg
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "video_repair_secret_key"

# Configuraciones
UPLOAD_FOLDER = 'uploads'
REPAIRED_FOLDER = 'repaired'
ALLOWED_EXTENSIONS = {'mp4', 'mpeg', 'flv', 'mov', 'avi', 'mkv', 'mpg'}

# Asegurar que las carpetas existan
for folder in [UPLOAD_FOLDER, REPAIRED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPAIRED_FOLDER'] = REPAIRED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def repair_video(input_path, output_path):
    """
    Intenta reparar un video usando remuxing primero y transcoding después si falla.
    """
    ffmpeg_path = r'C:\Users\Familia_Betancourt\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe' # <--- CAMBIA ESTO
    try:
        # Paso 1: Reparación rápida (Remuxing)
        # Intentamos copiar los flujos a un nuevo contenedor ignorando errores de cabecera
        print(f"Iniciando reparación rápida para: {input_path}")
        (
            ffmpeg
                .input(input_path, err_detect='ignore_err')
                .output(output_path, c='copy', map='0')
                # Añadimos cmd=ffmpeg_path para que no tenga que buscarlo
                .run(cmd=ffmpeg_path, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        return True, "Reparación rápida completada exitosamente (Remuxing)."
    except ffmpeg.Error as e:
        print("Remuxing falló, intentando reparación profunda (Transcoding)...")
        try:
            # Paso 2: Reparación profunda (Transcoding)
            # Forzamos la decodificación y recodificación de cada frame
            (
                ffmpeg
                .input(input_path)
                .output(output_path, vcodec='libx264', acodec='aac', strict='experimental')
                # También aquí
                .run(cmd=ffmpeg_path, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )
            return True, "Reparación profunda completada (Transcoding)."
        except ffmpeg.Error as e2:
            error_details = e2.stderr.decode() if e2.stderr else "Error desconocido de FFmpeg"
            print(f"Fallo total en la reparación: {error_details}")
            return False, f"No se pudo reparar el video: {error_details[:100]}..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        flash('No se seleccionó ningún archivo.')
        return redirect(request.url)
    
    file = request.files['video']
    if file.filename == '':
        flash('El nombre del archivo está vacío.')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = "repaired_" + filename
        output_path = os.path.join(app.config['REPAIRED_FOLDER'], output_filename)
        
        file.save(input_path)
        
        success, message = repair_video(input_path, output_path)
        
        if success:
            flash(message)
            return render_template('index.html', repaired_file=output_filename)
        else:
            flash(message)
            return redirect(url_for('index'))
            
    flash('Extensión de archivo no permitida.')
    return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['REPAIRED_FOLDER'], filename)

if __name__ == '__main__':
    # Asegurarse de tener ffmpeg instalado en el sistema
    app.run(debug=True, port=5000)
