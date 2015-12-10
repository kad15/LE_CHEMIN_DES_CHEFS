__author__ = 'IENAC15 - groupe 25'
#! /usr/bin/python
#-*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication

import vue
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f=vue.fenPrincipale()
    # f.show()
    sys.exit(app.exec_())