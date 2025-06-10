import sys
from PySide6.QtWidgets import QApplication
from qplayer_vlc import QPlayer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    vi1 = 'D:/SiSTEM/dance at home_2.mp4'
    wg = QPlayer()
    wg.setVolume(72)
    wg.show()
    wg.setVideo(vi1)
    sys.exit(app.exec())