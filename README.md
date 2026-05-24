# 🎥 Video Repair Tool

Una aplicación web potente y sencilla construida con Python y Flask para restaurar archivos de video corruptos utilizando el motor de FFmpeg.

## 🚀 Características
- **Reparación en dos niveles:** 
  1. **Remuxing:** Intenta arreglar el contenedor sin pérdida de calidad.
  2. **Transcoding:** Si el primero falla, reconstruye el flujo de video frame por frame.
- **Formatos soportados:** MP4, MPEG, FLV, MOV, AVI, MKV.
- **Interfaz moderna:** Diseño limpio basado en Bootstrap 5.
- **Seguridad:** Manejo seguro de archivos y nombres.

## 🛠️ Requisitos Previos

### 1. FFmpeg (Obligatorio)
Debes tener **FFmpeg** instalado en tu sistema y accesible desde la línea de comandos (agregado al PATH).
- **Windows:** [Descargar FFmpeg](https://ffmpeg.org/download.html#build-windows)
               `winget install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`

### 2. Python
- Python 3.7 o superior instalado.

## 📦 Instalación

1. Clona o descarga este proyecto.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

1. Inicia el servidor de Flask:
   ```bash
   python app.py
   ```
2. Abre tu navegador y navega a:
   `http://127.0.0.1:5000`
3. Selecciona tu archivo de video dañado y haz clic en **"Reparar Video Now!"**.
4. Una vez procesado, aparecerá un botón para descargar la versión reparada.

## 📂 Estructura del Proyecto
- `app.py`: Lógica del servidor y motor de reparación.
- `templates/`: Interfaz HTML.
- `uploads/`: Almacenamiento temporal de archivos subidos.
- `repaired/`: Almacenamiento de archivos listos para descargar.

## ⚠️ Nota sobre la reparación
La efectividad de la reparación depende del grado de corrupción del archivo. Si los datos binarios del video están completamente perdidos (ceros o datos aleatorios), es posible que no se pueda recuperar nada. Esta herramienta es ideal para archivos con índices rotos, cabeceras incompletas o cortes abruptos de grabación.
