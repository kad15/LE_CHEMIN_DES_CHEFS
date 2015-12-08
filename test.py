from PyQt5.QtGui import QIcon, QKeySequence

__author__ = 'risky'
#! /usr/bin/python3
#-*-coding: utf-8 -*-


from PyQt5.QtWidgets import *

class fenPrincipale(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        menuFichier = self.menuBar().addMenu("&Fichier")
        menuEdition = self.menuBar().addMenu("&Edition")
        menuAffichage = self.menuBar().addMenu("&Affichage")
        actionNouvelle = menuFichier.addAction("&Nouvelle partie")
        actionCharger= menuFichier.addAction("&Charger une partie")
        actionEnregistrer = menuFichier.addAction("&Enregistrer la partie")
        actionQuitter = menuFichier.addAction("&Quitter")
        actionQuitter.setIcon(QIcon("exit.png"))
        actionQuitter.setShortcut("Ctrl+Q")
        actionQuitter.setStatusTip('Exit application')
        actionQuitter.triggered.connect(qApp.quit)
        self.statusBar()
        self.setGeometry(1500, 1500, 1500, 1500)
        self.setWindowTitle('Le Chemin des chefs')
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(actionQuitter)

        zoneCentrale = QWidget()
        self.setCentralWidget(zoneCentrale)
        zoneCentrale.setStyleSheet("background-color:white;")
        self.show()
