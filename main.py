__author__ = 'IENAC15 - groupe 25'
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import view
from PyQt5.QtWidgets import QApplication





if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = view.Plateau()
    sys.exit(app.exec_())