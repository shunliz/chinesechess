from board import Board
from mcts.nodes import TwoPlayersGameState

import logging as log


class BoardPhase(TwoPlayersGameState):
    def __init__(self):
        self.board_status = [] 
        self.board_status.extend(Board.init_status)
        self.player = 0
        self.vRed = 0
        self.vBlack = 0
        self.PawnValue = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  9,  9,  9, 11, 13, 11,  9,  9,  9,  0,  0,  0,  0,
                          0,  0,  0, 19, 24, 34, 42, 44, 42, 34, 24, 19,  0,  0,  0,  0,
                          0,  0,  0, 19, 24, 32, 37, 37, 37, 32, 24, 19,  0,  0,  0,  0,
                          0,  0,  0, 19, 23, 27, 29, 30, 29, 27, 23, 19,  0,  0,  0,  0,
                          0,  0,  0, 14, 18, 20, 27, 29, 27, 20, 18, 14,  0,  0,  0,  0,
                          0,  0,  0,  7,  0, 13,  0, 16,  0, 13,  0,  7,  0,  0,  0,  0,
                          0,  0,  0,  7,  0,  7,  0, 15,  0,  7,  0,  7,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.KingValue = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0, 11, 15, 11,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.AdvisorValue = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0, 20,  0, 20,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0, 23,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0, 20,  0, 20,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.BishopValue = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0, 20,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0, 18,  0,  0,  0, 23,  0,  0,  0, 18,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0, 20,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.KnightValue = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0, 90, 90, 90, 96, 90, 96, 90, 90, 90,  0,  0,  0,  0,
                          0,  0,  0, 90, 96,103, 97, 94, 97,103, 96, 90,  0,  0,  0,  0,
                          0,  0,  0, 92, 98, 99,103, 99,103, 99, 98, 92,  0,  0,  0,  0,
                          0,  0,  0, 93,108,100,107,100,107,100,108, 93,  0,  0,  0,  0,
                          0,  0,  0, 90,100, 99,103,104,103, 99,100, 90,  0,  0,  0,  0,
                          0,  0,  0, 90, 98,101,102,103,102,101, 98, 90,  0,  0,  0,  0,
                          0,  0,  0, 92, 94, 98, 95, 98, 95, 98, 94, 92,  0,  0,  0,  0,
                          0,  0,  0, 93, 92, 94, 95, 92, 95, 94, 92, 93,  0,  0,  0,  0,
                          0,  0,  0, 85, 90, 92, 93, 78, 93, 92, 90, 85,  0,  0,  0,  0,
                          0,  0,  0, 88, 85, 90, 88, 90, 88, 90, 85, 88,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.RookValue = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,206,208,207,213,214,213,207,208,206,  0,  0,  0,  0,
                          0,  0,  0,206,212,209,216,233,216,209,212,206,  0,  0,  0,  0,
                          0,  0,  0,206,208,207,214,216,214,207,208,206,  0,  0,  0,  0,
                          0,  0,  0,206,213,213,216,216,216,213,213,206,  0,  0,  0,  0,
                          0,  0,  0,208,211,211,214,215,214,211,211,208,  0,  0,  0,  0,
                          0,  0,  0,208,212,212,214,215,214,212,212,208,  0,  0,  0,  0,
                          0,  0,  0,204,209,204,212,214,212,204,209,204,  0,  0,  0,  0,
                          0,  0,  0,198,208,204,212,212,212,204,208,198,  0,  0,  0,  0,
                          0,  0,  0,200,208,206,212,200,212,206,208,200,  0,  0,  0,  0,
                          0,  0,  0,194,206,204,212,200,212,204,206,194,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.CannonValue = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,100,100, 96, 91, 90, 91, 96,100,100,  0,  0,  0,  0,
                            0,  0,  0, 98, 98, 96, 92, 89, 92, 96, 98, 98,  0,  0,  0,  0,
                            0,  0,  0, 97, 97, 96, 91, 92, 91, 96, 97, 97,  0,  0,  0,  0,
                            0,  0,  0, 96, 99, 99, 98,100, 98, 99, 99, 96,  0,  0,  0,  0,
                            0,  0,  0, 96, 96, 96, 96,100, 96, 96, 96, 96,  0,  0,  0,  0,
                            0,  0,  0, 95, 96, 99, 96,100, 96, 99, 96, 95,  0,  0,  0,  0,
                            0,  0,  0, 96, 96, 96, 96, 96, 96, 96, 96, 96,  0,  0,  0,  0,
                            0,  0,  0, 97, 96,100, 99,101, 99,100, 96, 97,  0,  0,  0,  0,
                            0,  0,  0, 96, 97, 98, 98, 98, 98, 98, 97, 96,  0,  0,  0,  0,
                            0,  0,  0, 96, 96, 97, 99, 99, 99, 97, 96, 96,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.ChessValueTable = {0:self.KingValue,1:self.AdvisorValue,2:self.BishopValue,3:self.KnightValue,
                                4:self.RookValue,5:self.CannonValue,6:self.PawnValue}

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
                    if (chess_value == 19 or chess_value == 11) and not self.isSelfchess(chess_value) and self.board_status[Board.getKnightCheckedPin(src,dest)] == 0: #enemy knight and no pin
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
    
    def isDead(self):
        moves = []
        movecount, moves = self.GenerateMoves()
        if(movecount != 0):
            for move in moves:
                dest_chess_value = self.move_piece(move)
                if not self.isChecked():
                    self.undo_move_piece(move,dest_chess_value)
                    return False
                else:
                    self.undo_move_piece(move,dest_chess_value)   
            return True
        return False

    def __MOV(self,src,dest):
        return src+dest*256

    def GenerateMoves(self):
        #need check if still checked here to reduce the search space
        movs = []
        moveCount = 0
        for src in range(256):
            chess_value = self.board_status[src]
            if(self.isSelfchess(chess_value)):
                if chess_value == 18 or chess_value == 10: #Bishop
                    for delta in Board.BiShopDelta:
                        dest = src+delta
                        if self.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Bishop %d move: src %d, dest %d" %(chess_value,src,dest)
                elif chess_value == 9 or chess_value == 17: #Advisor
                    for delta in Board.AdvisorDelta:
                        dest = src+delta
                        if self.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Advisor %d move: src %d, dest %d" %(chess_value,src,dest)                    
                elif chess_value == 8 or chess_value == 16: #King
                    for delta in Board.KingDelta:
                        dest = src+delta
                        if self.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1  
                            #print "King %d move: src %d, dest %d" %(chess_value,src,dest)                 
                elif chess_value == 19 or chess_value == 11: #Knight
                    for delta in Board.KnightDeltaPin.keys():
                        dest = src+delta
                        if self.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Knight %d move: src %d, dest %d" %(chess_value,src,dest)                               
                elif chess_value == 20 or chess_value == 12: #Rook
                    for delta in Board.KingDelta:
                        dest = src+delta
                        while(Board.inBoard[dest]==1):
                            if self.isLegalMove(chess_value,src,dest):
                                movs.append(self.__MOV(src,dest))
                                moveCount = moveCount + 1
                                #print "Rook %d move: src %d, dest %d" %(chess_value,src,dest)   
                            dest = dest + delta
                elif chess_value == 21 or chess_value == 13: #Cannon
                    for delta in Board.KingDelta:
                        dest = src+delta
                        while(Board.inBoard[dest]==1):
                            if self.isLegalMove(chess_value,src,dest):
                                movs.append(self.__MOV(src,dest))
                                moveCount = moveCount + 1
                                #print "Cannon %d move: src %d, dest %d" %(chess_value,src,dest)   
                            dest = dest + delta                    
                elif chess_value == 22 or chess_value == 14: #Pawn
                    for delta in Board.KingDelta:
                        dest = src+delta
                        if self.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1 
                            #print "Pawn %d move: src %d, dest %d" %(chess_value,src,dest) 
        return moveCount, movs

    def __mirrorSquare(self,index):
        return 254 - index
    def __addPiece(self,index,chess_value):
        self.board_status[index] =  chess_value
        if chess_value < 16:
            self.vRed = self.vRed + self.ChessValueTable[chess_value - 8][index]
        else:
            self.vBlack = self.vBlack + self.ChessValueTable[chess_value - 16][self.__mirrorSquare(index)]
    def __delPiece(self,index,chess_value):
        self.board_status[index] =  0
        if chess_value < 16:
            self.vRed = self.vRed - self.ChessValueTable[chess_value - 8][index]
        else:
            self.vBlack = self.vBlack - self.ChessValueTable[chess_value - 16][self.__mirrorSquare(index)]   
                 
    def move_piece(self,move):
        src = move%256
        dest = int(move/256)
        dest_chess_value = self.board_status[dest]
        if dest_chess_value != 0:
            self.__delPiece(dest, self.board_status[dest])
        self.__addPiece(dest,self.board_status[src]) #move the piece to new place
        self.__delPiece(src, self.board_status[src]) # delete the piece in the original place
        return dest_chess_value     #return the dest piece for undo move. even it has no piece in dest, it will still return 0
    
    def undo_move_piece(self,move,dest_chess_value):
        src = move%256
        dest = int(move/256)
        temp = self.board_status[dest]
        self.__delPiece(dest, temp)
        self.__addPiece(src,temp)
        if dest_chess_value != 0:
            self.__addPiece(dest, dest_chess_value)
            
    def makeMove(self,move):
        temp = self.board_status[move%256]
        dest_chess_value = self.move_piece(move)
        if self.isChecked():
            self.undo_move_piece(move, dest_chess_value)
            return (False,0)
        self.changeSide()
        self.distance =  self.distance + 1
        log.info("Move chess %d, from %d to %d" %(temp,move%256,int(move/256)))
        return (True,dest_chess_value)
        
    def undoMakeMove(self,move,dest_chess_value):
        self.undo_move_piece(move,dest_chess_value)
        self.distance =  self.distance - 1
        self.changeSide()
        

class MCTSBoardPhase(BoardPhase):
    
    def __init__(self):
        super(MCTSBoardPhase, self).__init__()
    
    def is_game_over(self):
        return self.isDead();
    
    def get_legal_actions(self):
        return self.GenerateMoves()[1]
    
    def move(self, move):
        return self.move_piece(move)
    
    @property
    def game_result(self):
        if(self.is_game_over()):
            return 1
        
        return 0
    
    def is_move_legal(self, move):
        src = move%256
        dest = int(move/256)
        chess_value = self.board_status[src]
        return self.isLegalMove(chess_value, src, dest)
        