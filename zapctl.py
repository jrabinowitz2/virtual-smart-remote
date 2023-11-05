#!/usr/bin/env python3
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from zap_tx import ZapTX, ZapCommand

# CHANGE ME! See decoding_notes.txt to understand the protocol
FAN_ID = "111000001111100001101110000111111110011" # office
#FAN_ID = "111110011101011011111010010011000011110" # bedroom

class RadioWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, addr):
        super().__init__()
        self.tx = ZapTX()
        self.tx.set_addr(addr)

    def run(self, cmd):
        assert cmd

        self.tx.set_cmd(cmd)
        self.tx.restart()
        self.tx.run()
        self.tx.wait()
        self.finished.emit()

class CircleButton(QWidget):
    click = pyqtSignal(ZapCommand)

    def __init__(self, parent, name, debug=False):
        super().__init__(parent)

        self.name = name
        self.debug = debug
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def paintEvent(self, event=None):
        if not self.debug:
            return

        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.red)
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        print("PRESS:", self.name)
        self.click.emit(self.name)

class LightOverlay(QWidget):
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setOpacity(1.0)
        painter.setBrush(QColor(99, 130, 255))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())

class ZapGUI(QMainWindow):
    BUTTONS = [
        [ZapCommand.ON_1, 0.275, 0.191],
        [ZapCommand.OFF_1, 0.701, 0.191],
        [ZapCommand.ON_2, 0.275, 0.316],
        [ZapCommand.OFF_2, 0.701, 0.316],
        [ZapCommand.ON_ALL, 0.275, 0.679],
	[ZapCommand.OFF_ALL, 0.701, 0.679],
    ]
    LIGHT = [0.491, 0.113]

    def __init__(self):
        super().__init__()

        self.bg = QImage("img/zap-remote.png")
        self.setFixedSize(self.bg.size()*2)

        self.xmit = False
        self.light = LightOverlay(self)
        self.light.setVisible(False)

        self.worker = RadioWorker(FAN_ID)
        self.worker.finished.connect(self.radioDone)

        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()

        bounds = self.rect()
        dim = 33 #int(.1)
        ldim = 6 #int(.04)

        self.light.setGeometry(QRect(
            int(bounds.width()*ZapGUI.LIGHT[0]-ldim),
            int(bounds.height()*ZapGUI.LIGHT[1]-ldim),
            ldim*2, ldim*2))

        for name, x, y in ZapGUI.BUTTONS:
            button = CircleButton(self, name, debug=False)
            button.click.connect(self.handleButton)
            cx = int(bounds.width()*x)
            cy = int(bounds.height()*y)

            button.setGeometry(QRect(cx-dim, cy-dim, dim*2, dim*2))
            region = QRegion(0, 0, dim*2, dim*2, QRegion.Ellipse)
            button.setMask(region)

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.bg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    # Used for calculating button regions
    #def mousePressEvent(self, event):
    #    bounds = self.rect()
    #    pos = event.localPos()
    #    rpos = QPointF(pos.x()/bounds.width(), pos.y()/bounds.height())
    #    #print(rpos)

    def handleButton(self, cmd):
        if self.xmit:
            return

        self.light.setVisible(True)
        self.xmit = True
        self.light.repaint()
        self.callRadio(cmd)

    def callRadio(self, cmd):
        print("TX start...")
        self.worker.run(cmd)

    def radioDone(self):
        print("TX end!")
        self.xmit = False
        self.light.setVisible(False)

def main():
    app = QApplication(sys.argv)

    # Create the main window
    window = ZapGUI()

    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_NoSystemBackground, True)
    window.setAttribute(Qt.WA_TranslucentBackground, True)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
