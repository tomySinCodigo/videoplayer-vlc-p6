from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from skin import Ui_Form
import vlc


class QPlayer(QWidget, Ui_Form):
    def __init__(self, *args, **kw):
        super(QPlayer, self).__init__(*args, **kw)
        self.setupUi(self)
        self.__configQPlayer()
        
    def __configQPlayer(self):
        self.video_widget = QWidget()
        self.video_widget.setStyleSheet('background-color:black;')
        self.vly_video.addWidget(self.video_widget)

        vlc_args = [
            '--quiet',                    # Suprimir mensajes
            '--no-video-title-show',      # No mostrar título
            '--no-snapshot-preview',      # No preview de capturas
        ]
        self.instance = vlc.Instance(vlc_args)
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(int(self.video_widget.winId()))

        self.sld_time.setMaximum(1000)
        self.sld_vol.setMaximum(100)

        self.btn_play.clicked.connect(self.playPause)
        self.btn_stop.clicked.connect(self.stop)

    def setVideo(self, file:str):
        media = self.instance.media_new(file)
        self.player.set_media(media)

    def playPause(self):
        self.player.pause() if self.player.is_playing() else self.player.play()

    def stop(self):
        self.player.stop()

    def setPosition(self, pos):
        self.player.set_position(pos/1e3)

    def updatePos(self):
        if self.player.get_lenght() > 0:
            pos = self.player.get_position() * 1000
            self.sld_time.setValue(int(pos))

        current_time = self.player.get_time()
        total_time = self.player.get_lenght()
    
        # if current_time>=0 and total_time>0:
            # current_str = self.form



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    # vi1 = "D:/SiSTEM/my24res/Varios/Old man dancing.mp4"
    vi1 = 'D:/SiSTEM/dance at home_2.mp4'
    wg = QPlayer()
    wg.show()

    wg.setVideo(vi1)

    sys.exit(app.exec())