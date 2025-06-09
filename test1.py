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
        self.sld_time.sliderMoved.connect(self.setPosition)
        self.sld_vol.sliderMoved.connect(self.setVolume)
        self.btn_toggle.clicked.connect(self.toggleCtrl)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePos)
        self.timer.start(100)

        # CONFIGs
        self.setVolume(75)
        self.stw.setCurrentIndex(1)

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
        if self.player.get_length() > 0:
            pos:float = self.player.get_position() * 1000
            self.sld_time.setValue(int(pos))

        current_time:int = self.player.get_time()
        total_time:int = self.player.get_length()
    
        if current_time >= 0 and total_time > 0:
            current_str = self.ms_hms(current_time)
            self.lb_time.setText(current_str)
            self.lb_timestamp.setText(self.ms_hmsz(current_time))
            res = total_time - current_time
            self.lb_timestamp_res.setText(self.ms_hmsz(res))

    def _mseg_hmsz(self, milliseconds:float|str) -> tuple:
        '''retorna tupla[int] =  h, m, s, z'''
        h, r = divmod(float(milliseconds), 3.6e6)
        m, r = divmod(r, 6e4)
        s, z = divmod(r, 1e3)
        return int(h), int(m), int(s), int(z)
        
    def ms_hms(self, msec:int) -> str:
        timestamp = '00:00:00'
        if msec:
            h, m, s, z = self._mseg_hmsz(msec)
            timestamp = f'{h:02d}:{m:02d}:{s:02d}'
        return timestamp

    def ms_hmsz(self, msec:int) -> str:
        timestamp = '00:00:00.000'
        if msec:
            h, m, s, z = self._mseg_hmsz(msec)
            timestamp = f'{h:02d}:{m:02d}:{s:02d}.{z:03d}'
        return timestamp

    def setVolume(self, num:int):
        self.player.audio_set_volume(num)
        self.sld_vol.setValue(int(num))
        self.lb_vol.setText(str(num))

    def toggleCtrl(self):
        index:int = 0 if self.stw.currentIndex()==1 else 1
        self.stw.setCurrentIndex(index)





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