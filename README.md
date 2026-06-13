# 📹 Tapo Viewer: Visor y Grabador Flotante para Cámaras de Seguridad (RTSP)

![Tapo Viewer Interfaz - Visor Minimalista](screenshot.png)

**Tapo Viewer** es el mejor software gratuito, ligero y minimalista para monitorear y grabar cámaras de seguridad Tapo (y cualquier cámara compatible con protocolo RTSP) directamente desde tu PC con Windows. Desarrollado con Python, PyQt6 y el potente motor de video de VLC, es la alternativa perfecta a los visores pesados tradicionales.

## 🌟 Características Principales (Features)

*   **Interfaz Flotante y Sin Bordes (Picture-in-Picture)**: Monitorea tu cámara de seguridad en una esquina de tu monitor sin interrumpir tu trabajo. Diseño limpio, sin marcos molestos.
*   **Modo "Fijar por Encima" (Always on Top)**: Un botón integrado de chincheta (📌) mantiene el video visible sobre cualquier otra ventana, con transparencias nativas que evitan los bordes oscuros en Windows 10/11.
*   **Motor de Grabación Ultra-Robusto (RTSP-TCP)**: Graba el flujo de video en segundo plano sin afectar la visualización en vivo. Emplea el protocolo TCP forzado para asegurar 0 pérdida de paquetes y evitar archivos vacíos (0 KB) ocasionados por redes Wi-Fi inestables.
*   **Soporte Multi-Formato y Transcodificación Inteligente**: 
    *   Exporta a formatos `.ts`, `.mp4`, `.mkv` y `.avi`.
    *   El formato `.ts` te protege al 100% contra cortes de luz, evitando que el archivo de video se corrompa.
    *   *Conversión de Audio en Vivo*: Convierte automáticamente el códec propietario ALAW de las cámaras IP a MP3 universal si decides grabar "Con Audio".
*   **Anti-Colisión de Red (Gestión de Streams)**: Resuelve automáticamente el límite impuesto por las cámaras (Error de conexión simultánea). Si el grabador necesita la máxima resolución (2K Stream 1), el visor en miniatura cambiará de forma inteligente e imperceptible a 360p (Stream 2), evitando cuelgues.
*   **Programador Automático (Timer DVR)**: Convierte tu PC en un NVR/DVR. Configura rutinas de grabación con hora de inicio y fin para vigilar cuando no estás.
*   **Expansión Rápida (Doble Clic)**: Cambia de la vista de miniatura a pantalla completa en resolución 2K con un simple doble clic sobre el reproductor.

## ⚙️ Requisitos Previos

Para ejecutar la aplicación en tu entorno local o compilarla, es **obligatorio** contar con:
- **VLC Media Player**: El motor de video utiliza las librerías nativas de VLC para la decodificación por hardware del protocolo RTSP.
- **Python 3.x**: Solo necesario si deseas compilar o modificar el código fuente.

## 🚀 Instalación y Despliegue Rápido

El proyecto incluye scripts automatizados para instalar las dependencias con un solo clic.

1.  Clona o descarga este repositorio en tu equipo.
2.  Haz doble clic en el archivo `install_dependencies.bat`.
3.  El sistema instalará automáticamente VLC (vía `winget`) y todas las librerías de Python requeridas en `requirements.txt`.

## 💻 Guía de Uso

### Iniciar desde el código fuente
Para probar el proyecto de forma directa:
```bash
python main.py
```

### Generar la Versión Ejecutable (.exe Portátil)
Si deseas generar un ejecutable independiente para distribuirlo sin requerir Python:
1.  Ejecuta el archivo `build.bat`.
2.  Espera a que finalice el proceso de *PyInstaller*.
3.  Encontrarás tu aplicación lista y empaquetada en la carpeta `dist/Tapo Viewer.exe`.

## 🛠️ Controles y Ajustes

*   **Reubicar el visor**: Haz clic izquierdo y mantén presionado sobre el video para arrastrar la ventana por la pantalla.
*   **Grabación Manual**: Pulsa el botón `REC` visible en la esquina superior izquierda.
*   **Menú de Bandeja (System Tray)**: Busca el ícono negro de la cámara junto al reloj de Windows. Haz clic derecho para acceder a las opciones de "Configuración", "Iniciar con Windows", o "Acerca de".
*   **Conexión Inicial**: Ve a "Configuración" y completa la IP local de tu cámara (ej. `192.168.1.xxx`), el usuario y la contraseña (credenciales RTSP/ONVIF generadas en la app Tapo).

## 🧰 Stack Tecnológico
*   **PyQt6**: Gestión de interfaces GUI, overlay windows nativas y systray.
*   **python-vlc**: Wrapper de `libVLC` para el manejo avanzado de flujos de video IP (Decodificación por Hardware y transcodificación de red).
*   **PyInstaller**: Empaquetado binario.