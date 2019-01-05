import sys, os, pygame
from pygame.sprite import Sprite

class Chess(Sprite):
    chessImage = {8:os.path.join("RES", "RK.BMP"),9:os.path.join("RES", "RA.BMP"),
                  10:os.path.join("RES", "RB.BMP"),11:os.path.join("RES", "RN.BMP"),
                  12:os.path.join("RES", "RR.BMP"),13:os.path.join("RES", "RC.BMP"),
                  14:os.path.join("RES", "RP.BMP"),16:os.path.join("RES", "BK.BMP"),
                  17:os.path.join("RES", "BA.BMP"),18:os.path.join("RES", "BB.BMP"),
                  19:os.path.join("RES", "BN.BMP"),20:os.path.join("RES", "BR.BMP"),
                  21:os.path.join("RES", "BC.BMP"),22:os.path.join("RES", "BP.BMP"),}
    def __init__(self,chess_value):
        Sprite.__init__(self)
        self.chess_value = chess_value
        self.Image = self.__createChessImage()
        self.COLOR_KEY = (0,255,0)
        self.Image.set_colorkey(self.COLOR_KEY)
        self.isSelect = False
    def __createChessImage(self):
        return pygame.image.load(self.chessImage[self.chess_value]).convert()