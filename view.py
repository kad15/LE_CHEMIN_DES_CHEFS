__author__ = 'IENAC15 - groupe 25'
# ! /usr/bin/python3
# -*-coding: utf-8 -*-
import os

RESSOURCES = os.getcwd() + os.sep + "ressources" + os.sep
BACKUPS_DIR = os.getcwd() + os.sep + "game_backups" + os.sep

from constantes import *
from model import Jeu, load_jeu
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMainWindow, qApp, QPushButton, QLabel, \
    QFileDialog
from PyQt5.QtGui import QPainter, QPen, QPolygon, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QSize


def initialise_jeu(filename):
    """
    Crée la fenetre, le plateau et le pavage du plateau par des boutons transparents et affiche les pion
    :param filename: fichier avec les positions initiales des pions
    """
    l = list(load_jeu(RESSOURCES + filename))
    matrice_jeu = l[0]
    first_player = l[1]
    f = Window(first_player,
               matrice_jeu)  # crée la fenetre, le plateau et le pavage du plateau par des boutons tranparents
    f.draw_pions(matrice_jeu)  # trace les pions
    f.show()
    return f

class Window(QMainWindow):
    def __init__(self, first_player, matrice_jeu):
        super(Window, self).__init__()
        self.image_pion = {1: "pion1.png", 2: "pion2.png", 11: "chef1.png", 12: "chef2.png", 0: ""}
        self.winSize = min(QDesktopWidget().height(), QDesktopWidget().width())  # dim fenetre vs écran
        # print("self.winSize ", QDesktopWidget().height())
        self.ratioWinVsEcran = 1  # ratio d'occupation de la fenêtre vis à vis de l'écran
        self.resize(self.ratioWinVsEcran * self.winSize, self.ratioWinVsEcran * self.winSize)
        self.ratio = 0.70  # ratio plateau vs ecran
        self.taillePlateau = self.winSize * self.ratio
        self.marge = (self.winSize - self.taillePlateau) / 2  # marge fenêtre
        self.tailleCase = self.taillePlateau / 8
        self.decalage = self.tailleCase / 2
        self.setWindowIcon(QIcon(RESSOURCES + "logo_enac.png"))
        self.centrerSurEcran()
        self.initMenu()
        self.jeu = Jeu(first_player, matrice_jeu)
        self.affichePlayerCourant(self.jeu.player)
        # self.setFixedSize(self.ratioWinVsEcran * self.winSize, self.ratioWinVsEcran * self.winSize)  # pour avoir une fenêtre de taille fixée

    def initMenu(self):
        self.setWindowTitle('Le chemin des chefs - IENAC 15 - Groupe 25')
        self.setStatusTip("Cliquer sur le pion à déplacer puis sur la nouvelle position souhaitée.")
        self.setWindowIcon(QIcon(RESSOURCES + "logo_enac.png"))
        menuFichier = self.menuBar().addMenu("&Fichier")
        self.toolbar = self.addToolBar('')
        # menu et icône nouvelle partie
        actionNouvellePartie = menuFichier.addAction("&Nouvelle partie")
        self.toolbar.addAction(actionNouvellePartie)
        actionNouvellePartie.setShortcut("Ctrl+N")
        actionNouvellePartie.setStatusTip('Nouvelle partie')
        actionNouvellePartie.setIcon(QIcon(RESSOURCES + "new.png"))
        actionNouvellePartie.triggered.connect(lambda: self.nouvelle_partie())
        # menu et icône charger partie
        actionChargerPartie = menuFichier.addAction("&Charger une partie")
        actionChargerPartie.setIcon(QIcon(RESSOURCES + "folder.png"))
        actionChargerPartie.triggered.connect(lambda: self.chargerPartie())
        self.toolbar.addAction(actionChargerPartie)
        actionChargerPartie.setShortcut("Ctrl+C")
        actionChargerPartie.setStatusTip('Charger une partie')
        # menu et icône enregistrer partie
        actionEnregistrerPartie = menuFichier.addAction("&Enregistrer la partie")
        actionEnregistrerPartie.setIcon(QIcon(RESSOURCES + "save.png"))
        actionEnregistrerPartie.triggered.connect(lambda: self.enregistrerPartie())
        self.toolbar.addAction(actionEnregistrerPartie)
        actionEnregistrerPartie.setShortcut("Ctrl+E")
        actionEnregistrerPartie.setStatusTip("Sauvegarder la partie")
        # menu et icône aide
        menuAide = self.menuBar().addMenu("&?")
        actionRegle = menuAide.addAction("&Règles du jeu")
        actionRegle.setShortcut("Ctrl+R")
        actionRegle.setStatusTip('Règles du jeu')
        actionRegle.setIcon(QIcon(RESSOURCES + 'regle.png'))
        actionRegle.triggered.connect(lambda: self.ouvrirFichier("chemin_des_chefs.pdf"))
        self.toolbar.addAction(actionRegle)
        # menu et icone "recette logicielle"
        actionRecette = menuAide.addAction("Recette logicielle")
        actionRecette.setStatusTip('Document de recette logicielle')
        actionRecette.setIcon(QIcon(RESSOURCES + 'recette.png'))
        actionRecette.triggered.connect(lambda: self.ouvrirFichier("Recette.ods"))
        self.toolbar.addAction(actionRecette)
        # menu et icône quitter
        actionQuitter = menuFichier.addAction("&Quitter")
        actionQuitter.triggered.connect(qApp.quit)
        actionQuitter.setIcon(QIcon(RESSOURCES + "exit.png"))
        actionQuitter.setShortcut("Ctrl+Q")
        actionQuitter.setStatusTip('Quitter l\'application')
        self.statusBar()
        self.toolbar.addAction(actionQuitter)
        # Définition du central widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setGeometry(0, 0, self.winSize, self.winSize)
        # labels informant qui doit jouer
        self.haut = QLabel()
        self.haut.setParent(self.centralWidget)
        self.haut.setGeometry(self.taillePlateau / 2, self.marge / 3, 250, 20)
        self.bas = QLabel()
        self.bas.setParent(self.centralWidget)
        self.bas.setGeometry(self.taillePlateau / 2, self.winSize - self.marge, 250, 20)
        self.information = QLabel()
        self.information.setParent(self.centralWidget)
        self.information.setGeometry(0, 0, 250, 20)
        self.centralWidget.setParent(self)
        self.centralWidget.setGeometry(0, 0, self.winSize, self.winSize)
        self.centralWidget.setStyleSheet(BLANC)
        plateau = Plateau(self)
        # plateau.setParent(self.centralWidget)
        plateau.setGeometry(self.marge, self.marge, self.taillePlateau, self.taillePlateau)
        self.btn = {}  # dico des boutons qui effectuent un pavage, ou recouvrement, du plateau
        # chaque bouton symbolise une intersection dans la grille constituant le plateau de jeu.
        for i in range(0, N):
            for j in range(0, N):
                button = Button(self, i, j)
                # button.setParent(self.centralWidget)
                button.setToolTip(str(i) + "_" + str(j))
                self.btn[(i, j)] = button

    def nouvelle_partie(self):
        """crée un nouveau jeu sans créer une nouvelle fenêtre
        :param filename:
        :return:
        """
        l = list(load_jeu(RESSOURCES + "init_jeu.txt"))
        self.jeu.matrice_jeu = l[0]
        self.jeu.player = l[1]
        self.draw_pions(self.jeu.matrice_jeu)  # trace les pions
        self.affichePlayerCourant(self.jeu.player)

    def ouvrirFichier(self, filename):
        try:
            import webbrowser
            webbrowser.open_new_tab(RESSOURCES + filename)
        except Exception:
            print("Problème ouverture fichier ", filename)

    def chargerPartie(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Charger partie', BACKUPS_DIR)[0]
            l = list(load_jeu(filename))
            self.jeu.matrice_jeu = l[0]
            self.jeu.player = l[1]
            self.draw_pions(self.jeu.matrice_jeu)  # trace les pions
            self.affichePlayerCourant(self.jeu.player)
        except Exception:
            print("Abandon chargement jeu ou Problème en lien avec l'ouverture de fichier")

    def enregistrerPartie(self):
        try:
            filename = QFileDialog.getSaveFileName(self, 'enregistrerPartie', BACKUPS_DIR)[0]
            self.jeu.save_jeu(filename)
        except Exception:
            print("Problème lors de l'enregistrement du fichier")

    def affichePlayerCourant(self, num_joueur):
        """ Informe le joueur dont c'est le "tour" de jouer
        :param num_joueur: joueur 1 ou 2
        :return:
        """
        self.information.setText("")
        self.haut.setText("")
        self.bas.setText("")
        if num_joueur in (1, 2):
            txt = "A VOUS DE JOUER, JOUEUR {} !!!!!".format(num_joueur)
            if num_joueur == 1:
                self.haut.setText(txt)
            else:
                self.bas.setText(txt)

    def afficheInfo(self, txt, width=250):
        """
        :param txt: affiche le txt au dessus du plateau
        :return:
        """
        self.information.setGeometry(0, 0, width, 20)
        self.information.setStyleSheet('color: red')
        self.information.setText(txt)

    def centrerSurEcran(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def draw_pions(self, mat_jeu):
        """
        :param jeu: type list contenant des types Pions
        :return:
        """
        for i in range(N):
            for j in range(N):
                icon = QIcon()
                # utilisation de la méthode get() de la classe python dictionnaire pour la fonctionnalité valeur par défaut
                icon.addPixmap(QPixmap(RESSOURCES + self.image_pion.get(mat_jeu[i][j], "")), QIcon.Normal, QIcon.Off)
                self.btn[(i, j)].setIcon(icon)


class Plateau(QWidget):
    def __init__(self, win):
        super(Plateau, self).__init__(win)
        self.win = win

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPlateau(qp)
        qp.end()

    def drawPlateau(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, N):
            # qp.drawRect(i * self.win.tailleCase, 0, i * self.win.tailleCase, self.win.taillePlateau)
            # qp.drawRect(0, i * self.win.tailleCase, self.win.taillePlateau, i * self.win.tailleCase)
            qp.drawLine(i * self.win.tailleCase, 0, i * self.win.tailleCase, self.win.taillePlateau)
            qp.drawLine(0, i * self.win.tailleCase, self.win.taillePlateau, i * self.win.tailleCase)
        pen = QPen(PATH_COLOR, 6, Qt.SolidLine)
        qp.setPen(pen)
        l = []
        for pt in CHEMIN:
            l.append(QPoint(pt[0] * self.win.tailleCase, pt[1] * self.win.tailleCase))
            poly = QPolygon(l)
        qp.drawPolyline(poly)
        qp.setBrush(PATH_COLOR)
        a = self.win.tailleCase / 5
        b = a / 2
        qp.drawRect(4 * self.win.tailleCase - b, 4 * self.win.tailleCase - b, a, a)


class Button(QPushButton):
    def __init__(self, win, i, j):
        super(Button, self).__init__(win)
        self.i = i
        self.j = j
        self.win = win
        self.tailleBouton = self.win.tailleCase
        self.setGeometry(QRect(self.win.marge - self.win.decalage + self.win.tailleCase * i,
                               self.win.marge - self.win.decalage + self.win.tailleCase * j,
                               self.win.tailleCase, self.win.tailleCase))
        self.setFlat(True)
        self.setStyleSheet(TRANSPARENT)
        self.taillePion = int(self.win.tailleCase * 0.64)
        self.setIconSize(QSize(self.taillePion, self.taillePion))

    def mousePressEvent(self, event):
        event.accept()
        self.win.jeu.jouer(self.i, self.j)
        self.win.draw_pions(self.win.jeu.matrice_jeu)
        self.win.affichePlayerCourant(self.win.jeu.player)
        if self.win.jeu.winner() != '':
            self.win.affichePlayerCourant(3)  # efface l'annonce aux players
            self.win.afficheInfo(self.win.jeu.winner())
        elif self.win.jeu.info:
            self.win.afficheInfo(self.win.jeu.info, 2000)
