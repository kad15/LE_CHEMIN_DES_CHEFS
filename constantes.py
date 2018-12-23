from PyQt5.QtGui import QColor

N = 9  # 9 intersections  donc 8 cases

CHEMIN = [(4, 0), (5, 1), (5, 2), (5, 3), (6, 4), (7, 3),
          (7, 4), (8, 4), (7, 5), (8, 6), (7, 6), (7, 7),
          (6, 6), (5, 7), (5, 6), (4, 6), (5, 5), (4, 4),
          (3, 3), (4, 2), (3, 2), (3, 1), (2, 2), (1, 1),
          (1, 2), (0, 2), (1, 3), (0, 4), (1, 4), (1, 5),
          (2, 4), (3, 5), (3, 6), (3, 7), (4, 8)]

PATH_COLOR = QColor(0, 50, 250)
RED = QColor(255, 0, 0)
GREEN = QColor(0, 255, 0)
BLANC = "background-color:rgba(255,255,255,255);"
TRANSPARENT = "background-color: rgba(255,255,255,0) ;"
RED = "background-color:rgba(250,250,0,150);"

