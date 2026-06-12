# Tapo Viewer v3.0

Un visor ligero, flotante y minimalista para cámaras Tapo (y otras cámaras compatibles con RTSP), construido con Python, PyQt6 y VLC.

## Características Principales

- **Flotante y Minimalista**: Interfaz sin bordes, pensada para quedarse en una esquina de la pantalla sin estorbar.
- **Fijar por Encima (Always on Top)**: Un botón integrado de chincheta (📌) para mantener la cámara siempre visible por sobre otras ventanas. El diseño usa una capa transparente nativa de Windows para evitar bordes oscuros.
- **Grabación Ultra-Robusta**: Graba el flujo de video en segundo plano de manera simultánea sin afectar el rendimiento de visualización. Ahora utiliza el protocolo TCP para garantizar que no se pierdan fotogramas clave ni se generen archivos vacíos debido a inestabilidades del Wi-Fi.
- **Soporte Multi-Formato y Audio**: Exporta tus grabaciones a `.ts` (a prueba de fallos de energía y apagones), `.mp4`, `.mkv` y `.avi`. Elige si quieres grabar "Con Audio" (realizando una conversión inteligente de ALAW a MP3 al vuelo) o "Sin Audio".
- **Gestión Inteligente de Límite de Cámara**: Las cámaras Tapo rechazan conexiones duplicadas a la misma calidad. Tapo Viewer resolverá esto automáticamente para que el grabador pueda funcionar en 2K mientras se visualiza en 360p en modo ventana, sin que las conexiones colisionen.
- **Programador de Grabación (Timer)**: Configura una hora de inicio y fin automática; la aplicación se encargará de grabar tu cámara aunque no estés frente a la PC.
- **Doble Clic para Expandir**: Alterna rápidamente entre la visualización en ventana pequeña y pantalla completa (calidad 2K) haciendo doble clic en el video.
- **Configuración Dinámica**: Ajusta la IP de la cámara, credenciales RTSP, directorio de grabaciones y parámetros de visualización directamente desde la bandeja del sistema.

## Requisitos Previos

Para ejecutar la aplicación o compilarla, es **obligatorio** tener instalado:

- **VLC Media Player** (El motor de video utiliza las librerías nativas de VLC para conectarse al RTSP).
- **Python 3.x** (Solo si vas a correr o compilar el código fuente).

## Instalación Automática

Se incluye un script para facilitar la instalación del motor VLC y las librerías necesarias.

1. Clona o descarga este repositorio en tu PC.
2. Haz doble clic en el archivo install_dependencies.bat.
3. El script instalará automáticamente VLC usando winget y descargará las dependencias de Python listadas en equirements.txt.

## Uso

### A partir del código fuente
Puedes iniciar la aplicación directamente corriendo el script:
`ash
python main.py
`

### Versión Ejecutable (.exe)
Si prefieres generar un ejecutable .exe portátil que no requiera abrir la consola:

1. Ejecuta el archivo uild.bat.
2. Espera a que termine el proceso de PyInstaller.
3. Busca tu aplicación lista en la carpeta dist/Tapo Viewer.exe.

## Uso de la Aplicación

- **Mover la ventana**: Arrastra el video con el clic izquierdo del mouse para reubicarlo.
- **Grabar Video**: Haz clic en el botón REC o programa el temporizador desde los ajustes.
- **Ocultar/Ajustes**: Busca el ícono negro de la cámara en la bandeja de iconos (cerca de la hora en Windows). Haz clic derecho para ver las opciones de configuración.
- **Conectar tu cámara**: Ve a "Configuración" e introduce la IP local de tu cámara Tapo (ej. 192.168.1.41) y las credenciales RTSP.

## Tecnologías Utilizadas
- **PyQt6**: Creación de interfaz transparente sin bordes, overlay windows y manejo de eventos.
- **python-vlc**: Como *wrapper* de libVLC para reproducir y grabar (std/transcode) video RTSP con aceleración por hardware.
- **PyInstaller**: Empaquetado en un ejecutable autocontenido.