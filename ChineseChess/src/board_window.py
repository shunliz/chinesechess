import os, pygame
from board import Board
import logging as log

class BoardWindow():
    def __init__(self, computer_first=False):
        self.EDGE = 8
        self.SQUARE = 56
        self.WITH = 520
        self.HEIGHT = 576
        self.window = pygame.display.set_mode((self.WITH, self.HEIGHT))
        self.lastSelect = 0
        self.lastMov = 0
        self.COLOR_KEY = (0,255,0)
        pygame.display.set_caption('Chinese Chess') 
        self.boardImage = pygame.image.load(os.path.join("RES", "BOARD.BMP")).convert()
        self.selectImage = pygame.image.load(os.path.join("RES", "SELECTED.BMP")).convert()
        self.selectImage.set_colorkey(self.COLOR_KEY)
        self.screen = pygame.display.get_surface()
        self.computer_first = computer_first; 
        Board.init_chessList() 
    def __drawBoardBackgound(self):
        self.screen.blit(self.boardImage, (0, 0))   
    def __getWindowX(self,x):
        return (x-3)*self.SQUARE +self.EDGE
    def __getWindowY(self,y):
        return (y-3)*self.SQUARE +self.EDGE
    def __drawChess(self,chess,x,y,select=False):
        self.screen.blit(chess.Image,(self.__getWindowX(x),self.__getWindowY(y)))
        if select == True:
            self.screen.blit(self.selectImage,(self.__getWindowX(x),self.__getWindowY(y)))  
    def __XYtoBoardIndex(self,x,y):
        return x+y*16    

    def computer_move(self, boardPhase, chessEngine):
        mov = chessEngine.getBestMove(boardPhase)
        if not mov:
            log.info('Win')
            return False
        boardPhase.movePiece(mov % 256, int(mov / 256))
        return True


    def human_move(self, boardPhase, chessEngine, index):
        moved = False
        mov = boardPhase.movePiece(self.lastSelect, index)
        self.lastMov = mov
        self.lastSelect = 0
        if mov != 0:
            self.lastMov = mov
            self.lastSelect = 0
            if boardPhase.isDead(chessEngine):
                log.info("Win!")
                return
            moved = True
        return moved

    def boardClick(self,position,boardPhase,chessEngine):
        moved = False
        xx = position[0]
        yy = position[1]
        x = (xx - self.EDGE) / self.SQUARE + 3
        y = (yy - self.EDGE) / self.SQUARE + 3
        index = self.__XYtoBoardIndex(x, y)
        chess_value = boardPhase.board_status[index]
        if (chess_value != 0) and boardPhase.isSelfchess(chess_value):
            self.lastSelect = index
            self.__drawChess(Board.getChessItem(chess_value), x, y, True)
        if self.lastSelect != 0:
            if boardPhase.isLegalMove(boardPhase.board_status[self.lastSelect], self.lastSelect, index):
                moved = self.human_move(boardPhase, chessEngine, index)

            if moved and not self.computer_first:
                self.computer_move(boardPhase, chessEngine)
                        
    def drawBoard(self,boardPhase):
        self.__drawBoardBackgound()
        for x in range(Board.LEFT, Board.RIGHT+1):
            for y in range(Board.TOP,Board.BUTTOM+1):
                index = self.__XYtoBoardIndex(x,y)
                chess_value = boardPhase.board_status[index]
                if(chess_value != 0):
                    chess = Board.getChessItem(chess_value)
                    self.__drawChess(chess,x,y)         
                if(index == self.lastSelect)or (index == self.lastMov%256)or(index == self.lastMov/256):
                    self.screen.blit(self.selectImage,(self.__getWindowX(x),self.__getWindowY(y)))  
        pygame.display.flip()