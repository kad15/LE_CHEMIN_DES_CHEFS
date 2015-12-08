__author__ = 'risky'
#! /usr/bin/python
#-*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication

from test import fenPrincipale

import os,sys





if __name__ == '__main__':
    app = QApplication(sys.argv)
    f=fenPrincipale()
    f.show()
    sys.exit(app.exec_())