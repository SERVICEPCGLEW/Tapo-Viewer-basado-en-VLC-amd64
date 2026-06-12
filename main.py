import sys
import os
import winreg
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QSystemTrayIcon, QMenu, QFrame, QSizeGrip,
                             QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox,
                             QCheckBox, QComboBox, QTimeEdit, QGraphicsColorizeEffect, QTabWidget)
from PyQt6.QtCore import Qt, QPoint, QSettings, QSize, QTimer, QTime
from PyQt6.QtGui import QIcon, QAction, QFont, QGuiApplication
import vlc

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuracion de Camara")
        self.settings = QSettings("TapoViewer", "WindowSettings")
        
        layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tab_network = QWidget()
        self.tab_record = QWidget()
        self.tabs.addTab(self.tab_network, "Red / RTSP")
        self.tabs.addTab(self.tab_record, "Grabacion")
        
        # Red / RTSP Tab
        form_network = QFormLayout(self.tab_network)
        
        self.ip_input = QLineEdit(self.settings.value("rtsp_ip", "192.168.1.xxx"))
        self.user_input = QLineEdit(self.settings.value("rtsp_user", "admin"))
        self.pwd_input = QLineEdit(self.settings.value("rtsp_pwd", ""))
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        
        self.path2k_input = QLineEdit(self.settings.value("stream_1_path", "/stream1"))
        self.path360_input = QLineEdit(self.settings.value("stream_2_path", "/stream2"))
        
        form_network.addRow("IP / Hostname:", self.ip_input)
        form_network.addRow("Usuario RTSP:", self.user_input)
        form_network.addRow("Contrasena RTSP:", self.pwd_input)
        form_network.addRow("Ruta Alta Calidad (2K):", self.path2k_input)
        form_network.addRow("Ruta Baja Calidad (360p):", self.path360_input)
        
        # Grabacion Tab
        form_record = QFormLayout(self.tab_record)
        
        default_dir = os.path.join(os.path.expanduser("~"), "Videos", "TapoRecords")
        self.record_dir_input = QLineEdit(self.settings.value("record_dir", default_dir))
        
        self.record_quality = QComboBox()
        self.record_quality.addItem("Baja (360p) - Nativa", "stream2")
        self.record_quality.addItem("Media Baja (720p) - Comprimida", "stream1_720p")
        self.record_quality.addItem("Media Alta (1080p) - Comprimida", "stream1_1080p")
        self.record_quality.addItem("Maxima (Original 2K/1080p) - Nativa", "stream1")
        quality_idx = self.settings.value("record_quality_idx", 0, type=int)
        self.record_quality.setCurrentIndex(quality_idx)
        
        self.record_format = QComboBox()
        formats = ["mp4", "avi", "mkv", "ts"]
        self.record_format.addItems(formats)
        current_format = self.settings.value("record_format", "ts")
        if current_format in formats:
            self.record_format.setCurrentText(current_format)
            
        self.record_audio = QComboBox()
        self.record_audio.addItem("Sin Audio (Recomendado para evitar crashes)", False)
        self.record_audio.addItem("Con Audio (Riesgo con ALAW)", True)
        audio_val = self.settings.value("record_audio", False, type=bool)
        self.record_audio.setCurrentIndex(1 if audio_val else 0)
        
        self.schedule_checkbox = QCheckBox("Activar Grabacion Programada")
        self.schedule_checkbox.setChecked(self.settings.value("schedule_enabled", False, type=bool))
        
        self.time_start = QTimeEdit()
        self.time_start.setDisplayFormat("HH:mm")
        self.time_start.setTime(self.settings.value("schedule_start", QTime(8, 0), type=QTime))
        
        self.time_end = QTimeEdit()
        self.time_end.setDisplayFormat("HH:mm")
        self.time_end.setTime(self.settings.value("schedule_end", QTime(18, 0), type=QTime))
        
        form_record.addRow("Carpeta de Grabaciones:", self.record_dir_input)
        form_record.addRow("Calidad de Grabacion:", self.record_quality)
        form_record.addRow("Formato Contenedor:", self.record_format)
        form_record.addRow("Canal de Audio:", self.record_audio)
        form_record.addRow("", self.schedule_checkbox)
        form_record.addRow("Hora de Inicio:", self.time_start)
        form_record.addRow("Hora de Fin:", self.time_end)
        
        layout.addWidget(self.tabs)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def save_settings(self):
        self.settings.setValue("rtsp_ip", self.ip_input.text().strip())
        self.settings.setValue("rtsp_user", self.user_input.text().strip())
        self.settings.setValue("rtsp_pwd", self.pwd_input.text().strip())
        self.settings.setValue("stream_1_path", self.path2k_input.text().strip())
        self.settings.setValue("stream_2_path", self.path360_input.text().strip())
        
        self.settings.setValue("record_dir", self.record_dir_input.text().strip())
        self.settings.setValue("record_quality_idx", self.record_quality.currentIndex())
        self.settings.setValue("record_quality", self.record_quality.currentData())
        self.settings.setValue("record_format", self.record_format.currentText())
        self.settings.setValue("record_audio", self.record_audio.currentData())
        
        self.settings.setValue("schedule_enabled", self.schedule_checkbox.isChecked())
        self.settings.setValue("schedule_start", self.time_start.time())
        self.settings.setValue("schedule_end", self.time_end.time())
        
        self.accept()

class ButtonsOverlay(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.main_window = main_window

    def mousePressEvent(self, event):
        self.main_window.mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        self.main_window.mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        self.main_window.mouseReleaseEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        self.main_window.mouseDoubleClickEvent(event)

class TapoViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.settings = QSettings("TapoViewer", "WindowSettings")
        self.is_2k_mode = False
        self.is_always_on_top = self.settings.value("always_on_top", True, type=bool)
        self.old_pos = None

        self.setWindowTitle("Tapo Viewer")
        self.update_window_flags()

        saved_geometry = self.settings.value("geometry")
        if saved_geometry:
            self.restoreGeometry(saved_geometry)
        else:
            self.resize(640, 360)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.video_frame = QFrame(self.central_widget)
        self.video_frame.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.video_frame)

        self.overlay = ButtonsOverlay(self)

        self.pin_btn = QPushButton(self.overlay)
        self.pin_btn.setFixedSize(30, 30)
        self.pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pin_btn.clicked.connect(self.toggle_always_on_top)

        self.pin_layout = QVBoxLayout(self.pin_btn)
        self.pin_layout.setContentsMargins(0, 0, 0, 0)
        self.pin_label = QLabel("📌")
        self.pin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_label.setStyleSheet("background-color: transparent; font-size: 16px;")
        self.pin_layout.addWidget(self.pin_label)

        self.update_pin_style()
        
        self.is_recording = False
        self.is_auto_recording = False
        self.record_player = None
        self.record_vlc_instance = None
        
        self.rec_btn = QPushButton("REC", self.overlay)
        self.rec_btn.setFixedSize(50, 30)
        self.rec_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rec_btn.clicked.connect(self.toggle_recording)
        self.update_rec_style()

        self.size_grip = QSizeGrip(self.central_widget)
        self.size_grip.setStyleSheet("background-color: rgba(255, 255, 255, 50); width: 15px; height: 15px;")
        self.size_grip.setFixedSize(15, 15)

        self.init_vlc()

        self.tray_icon = QSystemTrayIcon(self)
        
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icon.png")
        else:
            icon_path = "icon.png"
            
        self.tray_icon.setIcon(QIcon(icon_path))
        
        tray_menu = QMenu()
        
        self.show_hide_action = QAction("Ocultar", self)
        self.show_hide_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(self.show_hide_action)

        self.always_on_top_action = QAction("Fijar por encima", self, checkable=True)
        self.always_on_top_action.setChecked(self.is_always_on_top)
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top_action)
        tray_menu.addAction(self.always_on_top_action)
        
        self.startup_action = QAction("Iniciar con Windows", self, checkable=True)
        self.startup_action.setChecked(self.check_startup())
        self.startup_action.triggered.connect(self.toggle_startup)
        tray_menu.addAction(self.startup_action)
        
        config_action = QAction("Configuración", self)
        config_action.triggered.connect(self.open_config)
        tray_menu.addAction(config_action)
        
        quit_action = QAction("Cerrar", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.play_stream(self.get_stream_url(self.is_2k_mode))
        
        self.schedule_timer = QTimer(self)
        self.schedule_timer.timeout.connect(self.check_schedule)
        self.schedule_timer.start(60000)
        QTimer.singleShot(1000, self.check_schedule)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None and not self.is_2k_mode:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = None

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            QTimer.singleShot(0, self.toggle_2k_mode)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'size_grip'):
            self.size_grip.move(self.width() - self.size_grip.width(), self.height() - self.size_grip.height())
        if hasattr(self, 'overlay') and hasattr(self, 'pin_btn') and hasattr(self, 'rec_btn'):
            self.overlay.setGeometry(self.geometry())
            self.pin_btn.move(self.overlay.width() - self.pin_btn.width() - 5, 5)
            self.rec_btn.move(self.overlay.width() - self.pin_btn.width() - self.rec_btn.width() - 15, 5)

    def moveEvent(self, event):
        super().moveEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(self.geometry())

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.show()

    def update_window_flags(self):
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self.is_always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        if hasattr(self, 'central_widget'):
            self.show()

    def update_pin_style(self):
        effect = QGraphicsColorizeEffect(self.pin_label)
        if self.is_always_on_top:
            effect.setColor(Qt.GlobalColor.red)
        else:
            effect.setColor(Qt.GlobalColor.white)
        self.pin_label.setGraphicsEffect(effect)
        self.pin_btn.setStyleSheet("background-color: rgba(255, 255, 255, 100); border-radius: 15px; border: none;")

    def toggle_always_on_top(self):
        self.is_always_on_top = not self.is_always_on_top
        self.settings.setValue("always_on_top", self.is_always_on_top)
        self.always_on_top_action.setChecked(self.is_always_on_top)
        self.update_pin_style()
        self.update_window_flags()

    def toggle_always_on_top_action(self, checked):
        self.is_always_on_top = checked
        self.settings.setValue("always_on_top", self.is_always_on_top)
        self.update_pin_style()
        self.update_window_flags()

    def update_rec_style(self):
        if self.is_recording:
            self.rec_btn.setStyleSheet("background-color: rgba(255, 0, 0, 180); color: white; border-radius: 15px; font-weight: bold; border: none;")
        else:
            self.rec_btn.setStyleSheet("background-color: rgba(128, 128, 128, 150); color: white; border-radius: 15px; font-weight: bold; border: none;")

    def check_schedule(self):
        if not self.settings.value("schedule_enabled", False, type=bool):
            if self.is_recording and self.is_auto_recording:
                self.stop_recording()
            return
            
        start_time = self.settings.value("schedule_start", QTime(8, 0), type=QTime)
        end_time = self.settings.value("schedule_end", QTime(18, 0), type=QTime)
        current_time = QTime.currentTime()
        
        is_in_range = False
        if start_time < end_time:
            is_in_range = start_time <= current_time <= end_time
        else:
            is_in_range = current_time >= start_time or current_time <= end_time
            
        if is_in_range and not self.is_recording:
            self.is_auto_recording = True
            self.start_recording()
        elif not is_in_range and self.is_recording and self.is_auto_recording:
            self.stop_recording()
            self.is_auto_recording = False

    def toggle_recording(self):
        self.is_auto_recording = False 
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        if self.is_recording: return
        
        default_dir = os.path.join(os.path.expanduser("~"), "Videos", "TapoRecords")
        rec_dir = self.settings.value("record_dir", default_dir)
        os.makedirs(rec_dir, exist_ok=True)
        
        format_str = self.settings.value("record_format", "ts")
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Tapo_{now}.{format_str}"
        filepath = os.path.join(rec_dir, filename).replace('\\', '/')
        
        
        quality = self.settings.value("record_quality", "stream1")
        
        ip = self.settings.value("rtsp_ip", "192.168.1.xxx")
        user = self.settings.value("rtsp_user", "admin")
        pwd = self.settings.value("rtsp_pwd", "")
        
        vlc_args = [
            "--avcodec-hw=any", 
            "--drop-late-frames",
            "--rtsp-tcp",
            "--network-caching=1000"
        ]
        
        audio_enabled = self.settings.value("record_audio", False, type=bool)
        if not audio_enabled:
            vlc_args.append("--no-sout-audio")
            
        self.record_vlc_instance = vlc.Instance(*vlc_args)
        self.record_player = self.record_vlc_instance.media_player_new()
        
        audio_sout = "acodec=mp3,ab=128,channels=2,samplerate=44100" if audio_enabled else ""
        
        if quality == "stream1_720p":
            video_sout = "vcodec=h264,vb=1500,scale=Auto,width=1280,height=720"
            if audio_sout:
                sout = f"#transcode{{{video_sout},{audio_sout}}}:std{{access=file,mux={format_str},dst='{filepath}'}}"
            else:
                sout = f"#transcode{{{video_sout}}}:std{{access=file,mux={format_str},dst='{filepath}'}}"
            stream_url = f"rtsp://{user}:{pwd}@{ip}:554/stream1"
        elif quality == "stream1_1080p":
            video_sout = "vcodec=h264,vb=3000,scale=Auto,width=1920,height=1080"
            if audio_sout:
                sout = f"#transcode{{{video_sout},{audio_sout}}}:std{{access=file,mux={format_str},dst='{filepath}'}}"
            else:
                sout = f"#transcode{{{video_sout}}}:std{{access=file,mux={format_str},dst='{filepath}'}}"
            stream_url = f"rtsp://{user}:{pwd}@{ip}:554/stream1"
        else:
            if audio_sout:
                sout = f"#transcode{{{audio_sout}}}:std{{access=file,mux={format_str},dst='{filepath}'}}"
            else:
                sout = f"#std{{access=file,mux={format_str},dst='{filepath}'}}"
            stream_url = f"rtsp://{user}:{pwd}@{ip}:554/{quality}"

        from PyQt6.QtWidgets import QMessageBox
        if "stream1" in stream_url and self.is_2k_mode:
            QMessageBox.warning(self, "Límite de la Cámara", "Las cámaras Tapo no permiten visualizar y grabar la máxima calidad (2K) al mismo tiempo en el mismo equipo.\n\nPara poder grabar sin fallos (archivos de 0 KB), el visor en vivo cambiará automáticamente a calidad baja (360p).")
            self.toggle_visibility()
        import time
        time.sleep(1) # Dale 1 segundo a la camara para liberar el socket de stream1
            
        try:
            with open(os.path.join(rec_dir, "debug.log"), "w") as f:
                f.write(f"stream_url: {stream_url}\n")
                f.write(f"sout: {sout}\n")
        except:
            pass

        self.record_player.set_mrl(stream_url, f":sout={sout}")
        self.record_player.play()
        
        self.is_recording = True
        self.update_rec_style()

    def stop_recording(self):
        if not self.is_recording: return
        
        if self.record_player:
            self.record_player.stop()
            self.record_player.release()
            self.record_player = None
        if self.record_vlc_instance:
            self.record_vlc_instance.release()
            self.record_vlc_instance = None
            
        self.is_recording = False
        self.update_rec_style()

    def init_vlc(self):
        user = self.settings.value("rtsp_user", "admin")
        pwd = self.settings.value("rtsp_pwd", "")
        
        if hasattr(self, 'player') and self.player is not None:
            self.player.stop()

        self.vlc_instance = vlc.Instance(
            "--avcodec-hw=any",
            "--drop-late-frames",
            "--rtsp-tcp",
            "--network-caching=500",
            f"--rtsp-user={user}",
            f"--rtsp-pwd={pwd}"
        )
        self.player = self.vlc_instance.media_player_new()
        self.player.set_hwnd(int(self.video_frame.winId()))
        self.player.video_set_mouse_input(False)
        self.player.video_set_key_input(False)
        
    def get_stream_url(self, is_2k):
        ip = self.settings.value("rtsp_ip", "192.168.1.xxx")
        if is_2k:
            path = self.settings.value("stream_1_path", "/stream1")
        else:
            path = self.settings.value("stream_2_path", "/stream2")
        # Ensure path starts with /
        if not path.startswith("/"):
            path = "/" + path
        return f"rtsp://{ip}:554{path}"

    def play_stream(self, url):
        if hasattr(self, 'player') and self.player is not None:
            self.player.stop()
            
        media = self.vlc_instance.media_new(url)
        self.player.set_media(media)
        self.player.play()
        self.player.audio_set_mute(True)

    def open_config(self):
        dialog = ConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Restart stream with new settings
            self.init_vlc()
            url = self.get_stream_url(self.is_2k_mode)
            self.play_stream(url)
            self.check_schedule()

    def toggle_2k_mode(self):
        if not self.is_2k_mode:
            self.is_2k_mode = True
            self.overlay.hide()
            self.showFullScreen()
        else:
            self.is_2k_mode = False
            self.showNormal()
            self.overlay.show()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            self.show_hide_action.setText("Mostrar")
        else:
            self.show()
            self.show_hide_action.setText("Ocultar")

    def check_startup(self):
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_READ) as registry_key:
                value, _ = winreg.QueryValueEx(registry_key, "TapoViewer")
                return True
        except FileNotFoundError:
            return False

    def toggle_startup(self, state):
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        exe_path = os.path.abspath(sys.argv[0])
        if exe_path.endswith('.py'):
            command = f'"{sys.executable}" "{exe_path}"'
        else:
            command = f'"{exe_path}"'
            
        try:
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_WRITE) as registry_key:
                if state:
                    winreg.SetValueEx(registry_key, "TapoViewer", 0, winreg.REG_SZ, command)
                else:
                    winreg.DeleteValue(registry_key, "TapoViewer")
        except Exception as e:
            print(f"Error toggling startup: {e}")

    def closeEvent(self, event):
        if not self.is_2k_mode:
            self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)

    def quit_app(self):
        if self.is_recording:
            self.stop_recording()
        self.player.stop()
        self.close()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    viewer = TapoViewer()
    viewer.show()
    sys.exit(app.exec())
