#encoding: utf-8
import sys, os, pygame
from pygame.locals import * 
from pygame.sprite import Sprite
from ChessEngine import *
import copy

import logging as log


pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init() 

     
class BoardPhase():
    def __init__(self):
        self.board_status = [] 
        self.board_status.extend(Board.init_status)
        self.player = 0
        return
    def movePiece(self,srcPos,desPos):
        value = self.board_status[srcPos]
        self.board_status[srcPos] = 0
        dest_value =  self.board_status[desPos]
        self.board_status[desPos] = value
        if self.isChecked():
            self.board_status[srcPos] = self.board_status[desPos]
            self.board_status[desPos] = dest_value
            return 0
        else:
            self.changeSide()
            return srcPos + desPos*256
    def changeSide(self):
        self.player  =  1 -  self.player
    def setSide(self,side):
        self.player =  side
    def getSide(self):
        return self.player
    def reset(self):
        self.board_status = [] 
        self.board_status.extend(Board.init_status)
        self.player = 0
    def isSelfchess(self,chess_value):
        if((chess_value & 8)!= 0) and (self.getSide() == 0):
            return True
        if((chess_value & 16)!= 0) and (self.getSide() == 1):
            return True
        return False
    def isLegalMove(self,chess_value,src,dest):
        if self.isSelfchess(chess_value):
            if chess_value == 18 or chess_value == 10: #Bishop
                delta =  dest - src
                if Board.inBoard[dest]== 1 and not self.isSelfchess(self.board_status[dest]) and Board.isSameHalf(src,dest) and delta in Board.BiShopDelta and self.board_status[Board.getBishopPin(src,dest)]==0:                    
                    return True 
                return False
            if chess_value == 9 or chess_value == 17: #Advisor
                delta =  dest - src
                if Board.inFort[dest] == 1 and not self.isSelfchess(self.board_status[dest]) and delta in Board.AdvisorDelta:
                    return True
                return False
            if chess_value == 8 or chess_value == 16: #King
                delta =  dest - src
                if Board.inFort[dest] == 1 and not self.isSelfchess(self.board_status[dest]) and delta in Board.KingDelta:
                    return True
                return False
            if chess_value == 19 or chess_value == 11: #Knight
                delta =  dest - src
                if Board.inBoard[dest] == 1 and not self.isSelfchess(self.board_status[dest]) and delta in Board.KnightDeltaPin.keys() and self.board_status[Board.getKnightPin(src,dest)]==0:
                    return True
                return False
            if chess_value == 20 or chess_value == 12: #Rook
                pin = 0
                if Board.inBoard[dest] != 1 or  self.isSelfchess(self.board_status[dest]): #out side the board or the dest square has a self-side chess
                    return False
                delta =  dest - src
                if Board.isSameRow(src,dest):
                    if delta < 0:
                        delta = -1
                    else:
                        delta = 1
                elif Board.isSameColum(src,dest):
                    if delta < 0:
                        delta = -16
                    else:
                        delta = 16
                else:
                    return False
                pin =  src + delta
                while(pin != dest and self.board_status[pin] == 0):
                    pin = pin +delta
                if(pin == dest):
                    return True               
                return False
            if chess_value == 21 or chess_value == 13: #Cannon
                pin = 0
                if Board.inBoard[dest] != 1: #out side the board
                    return False
                delta =  dest - src
                if Board.isSameRow(src,dest):
                    if delta < 0:
                        delta = -1
                    else:
                        delta = 1
                elif Board.isSameColum(src,dest):
                    if delta < 0:
                        delta = -16
                    else:
                        delta = 16
                else:
                    return False
                pin =  src + delta
                while(pin != dest and self.board_status[pin] == 0):
                    pin = pin +delta
                if pin == dest: 
                    if self.board_status[pin] == 0:
                        return True
                    else:
                        return False 
                else:
                    if self.board_status[dest] != 0 and not self.isSelfchess(self.board_status[dest]) :
                        pin = pin + delta
                        while(pin != dest and self.board_status[pin] == 0):
                            pin = pin + delta
                        if pin == dest:
                            return True
                        else:
                            return False                   
                return False
            if chess_value == 22 or chess_value == 14: #Pawn
                delta =  dest - src
                if self.isSelfchess(self.board_status[dest]) :
                    return False
                if Board.inBoard[dest] == 1:
                    if Board.isCrossRiver(dest,self.getSide()) and (delta == -1 or delta == 1):
                        return True
                    else:
                        if self.getSide() == 0 and delta == -16:
                            return True
                        if self.getSide() == 1 and delta == 16:
                            return True
                        return False
                else:  
                    return False                       
        return False
    def isChecked(self):
        for src in range(256):
            chess_value = self.board_status[src]
            if (chess_value == 8 or chess_value == 16) and  self.isSelfchess(chess_value):  #find out the self side King
                #Judge if king is checked by Pawn
                if self.getSide()== 0: #if self is Red side
                    for delta in (-1,1,-16):
                        chess_value = self.board_status[src+delta]
                        if chess_value == 22: #enemy Pawn
                            log.info("checked by Pawn")
                            return True
                else:  #if self is Black side
                    for delta in (-1,1,16):  #enemy Pawn
                        chess_value = self.board_status[src+delta]
                        if chess_value == 14:
                            log.info("checked by Pawn")
                            return True
                #Judge if king is checked by Knight
                for delta in  Board.KnightDeltaPin.keys():
                    dest = src + delta
                    chess_value = self.board_status[dest]
                    if (chess_value == 19 or chess_value == 11) and not self.isSelfchess(chess_value) and boardPhase.board_status[Board.getKnightCheckedPin(src,dest)] == 0: #enemy knight and no pin
                        log.info("checked by Knight")
                        return True 
                #Judge if king is checked by Rook or King
                for delta in Board.KingDelta:
                    dest = src + delta
                    while(Board.inBoard[dest]==1):
                        chess_value = self.board_status[dest]
                        if(chess_value != 0):
                            if(chess_value == 20 or chess_value == 12 or chess_value == 16 or chess_value == 8) and not self.isSelfchess(chess_value): #enemy Rook or king
                                log.info("checked by Rook or king")
                                return True
                            else:
                                break
                        else:
                            dest = dest +delta

                #Judge if king is checked by Canon
                for delta in Board.KingDelta:
                    dest = src + delta
                    while(Board.inBoard[dest]==1):
                        chess_value = self.board_status[dest]
                        if(chess_value != 0):
                            break                                     
                        else:
                            dest =  dest + delta 
                    dest =  dest + delta
                    while(Board.inBoard[dest]==1):
                        chess_value = self.board_status[dest]
                        if(chess_value != 0):
                            if(chess_value == 21 or chess_value == 13) and not self.isSelfchess(chess_value): #enemy Canon
                                log.info("chessvalue %d, side %d checked by Canon" %(chess_value,self.getSide()))
                                return True
                            else:
                                break
                        else:
                            dest = dest +delta                      
                return False
        return False
    def isDead(self,chessEngine):
        moves = []
        movecount = chessEngine.GenerateMoves(self,moves)
        if(movecount != 0):
            for move in moves:
                dest_chess_value = chessEngine.move_piece(self,move)
                if not self.isChecked():
                    chessEngine.undo_move_piece(self,move,dest_chess_value)
                    return False
                else:
                    chessEngine.undo_move_piece(self,move,dest_chess_value)   
            return True
        return False
   
class BoardWindow():
    def __init__(self):
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
        x = (xx - boardWindow.EDGE) / boardWindow.SQUARE + 3
        y = (yy - boardWindow.EDGE) / boardWindow.SQUARE + 3
        index = self.__XYtoBoardIndex(x, y)
        chess_value = boardPhase.board_status[index]
        if (chess_value != 0) and boardPhase.isSelfchess(chess_value):
            self.lastSelect = index
            self.__drawChess(Board.getChessItem(chess_value), x, y, True)
        if self.lastSelect != 0:
            if boardPhase.isLegalMove(boardPhase.board_status[self.lastSelect], self.lastSelect, index):
                moved = self.human_move(boardPhase, chessEngine, index)

            if moved and not computer_first:
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
                  
def input(events,boardWindow,chessEngine): 
    for event in events: 
        if event.type == QUIT:
            chessEngine.save()
            sys.exit(0) 
        elif event.type == MOUSEBUTTONDOWN:
            boardWindow.boardClick(pygame.mouse.get_pos(),boardPhase,chessEngine)
            return
        else:
            pass
"""
        elif event.type == KEYDOWN:
            if event.mod & KMOD_CTRL and event.key == 102:
                for i in range(50,128):
                    tmp = boardPhase.board_status[i]
                    boardPhase.board_status[i]= boardPhase.board_status[254-i]
                    boardPhase.board_status[254-i]=tmp
                if boardPhase.player == 0:
                    boardPhase.player = 1
                else:
                    boardPhase.player = 0
            return     
"""

boardWindow = BoardWindow()
boardPhase = BoardPhase()
boardWindow.drawBoard(boardPhase)
chessEngine =  ChessEngine()
computer_first = False
stop = False
train_flag = True
while True:
    if train_flag:
        pygame.event.pump()
        ret = boardWindow.computer_move(boardPhase, chessEngine)
        if not ret:
            boardPhase.reset()
    else:
        if computer_first and boardPhase.getSide()==0 and not stop:
            if not boardWindow.computer_move(boardPhase, chessEngine):
                stop = True
        input(pygame.event.get(),boardWindow,chessEngine)
    boardWindow.drawBoard(boardPhase)
    pygame.display.flip()

if train_flag:
   chessEngine.save()
