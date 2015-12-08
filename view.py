__author__ = 'IENAC15 - groupe 25'
#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
sys.path.insert(0, sys.path[0] + "/data/")
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGraphicsEllipseItem, QMainWindow, QGraphicsScene,QGraphicsView
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QIcon
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtSvg import *

N = 9 # 9 intersections  donc 8 cases
RATIO = 0.9 # ratio d'occupation de la fenêtre vis à vis de l'écran
PATH_COLOR = QColor(0, 50, 250)
RED = QColor(255, 0, 0)
GREEN = QColor(0,255,0)

class Plateau(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        winSize = RATIO * QDesktopWidget().height()
        self.resize(winSize, winSize)
        self.center()
        self.setWindowTitle('Le chemin des chefs')
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QIcon(sys.path[0] + 'general.png'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPlateau(qp)
        qp.end()

    def drawPlateau(self, qp):
        winSize = min(self.height(), self.width())
        marge = winSize / 20
        step = (winSize - 2 * marge) / (N - 1) # taille d'une case
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, N):
            qp.drawLine(marge + i * step, marge, marge + i * step, winSize - marge)
            qp.drawLine(marge, marge + i * step, winSize - marge, marge + i * step)
        pen = QPen(Qt.blue, 6, Qt.SolidLine)
        pen.setBrush(PATH_COLOR)
        qp.setPen(pen)
        chemin = self.chiefPath
        l = []
        for pt in chemin:
            l.append(QPoint(marge + pt[0] * step, marge + pt[1] * step))
            poly = QPolygon(l)
        qp.drawPolyline(poly)
        qp.setBrush(PATH_COLOR)
        a = step / 5
        b = a / 2
        qp.drawRect(marge + 4 * step - b, marge + 4 * step - b, a, a)
        d = step/3
        qp.setBrush(RED)
        pen.setWidth(0)
        qp.setPen(pen)
        qp.drawEllipse(marge, marge, d, d)



    @property
    def chiefPath(self):
        ''' calcul of the chiefs path considering its symmetry
        :return:chiefs' path as a list ; top left corner position is (0, 0)
        '''
        chemin = [(4,0),(5,1), (5,3), (6,4),(7,3), \
                  (7,4),(8,4),(7,5),(8,6),(7,6),(7,7),\
                  (6,6),(5,7),(5,6),(4,6),(5,5), (4,4)]
        ch2 = []
        for pt in chemin:
            ch2.append((8 - pt[0], 8 - pt[1]))  # car le chemin est symétrique de centre (4,4)
        ch2.pop()
        ch2.reverse()
        return chemin + ch2

    def drawPions(self, qp):
        pass



class Pions(QGraphicsEllipseItem):

    def __init__(self, color, x, y, diameter):
        super(Pions, self).__init__(None)
        self.setBrush(color)
        d = diameter / 2
        self.setRect(x - d, y - d, d, d)

    def mousePressEvent(self, event):
            super().mousePressEvent(event)

            event.accept()
            self.moving.radarview.ask_inspection(self.flight)

            self.route_item = self.add_flight_route()
            self.state = self.state_dragging

    def mouseReleaseEvent(self,
                          event):  # reçu même si en dehors de l'item ! spécialité de Qt, qui permet la localité du code
        super().mouseReleaseEvent(event)

        if self.state == self.state_dragging:
            event.accept()
            self.remove_flight_route()
            self.state = self.state_idle

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self.state == self.state_dragging:
            event.accept()



