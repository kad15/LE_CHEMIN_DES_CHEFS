__author__ = 'IENAC15 - groupe 25'


class  Pion:

    def __index__(self):

        type = 0 # 0 : pion de type invisible 1 ou 2 : type joueur 1 ou 2
        # position = i, j
        self.isChef = False

class Position:
    """
    Position i, j sur la matrice du jeu ; top left (0, 0) bottom right (8, 8)
    """
    def __init__(self, i, j):
        self.i = i
        self.j = j



# def load_game(file):
#     dico = {}
#     with open(file,'r') as f:
#         for line in f:
#             param = line.strip().split()
#             point = Point(int(param[1]), int(param[2]))
#             dico[param[0]] = point
#     return dico

