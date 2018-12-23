__author__ = 'IENAC15 - groupe 25'
# ! /usr/bin/python
# -*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication
from view import Window, initialise_jeu
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = initialise_jeu("init_jeu.txt")

    # fichier de test de la capture max
    # initialise_jeu("../game_backups/00_testCaptureMax.txt")

    sys.exit(app.exec_())
