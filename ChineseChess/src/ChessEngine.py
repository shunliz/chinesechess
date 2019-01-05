#encoding: utf-8
import time
import copy
from random import choice
from math import sqrt, log
from board import Board
from mcts.nodes import *
from mcts.search import *

import logging

class ChessEngine():
    def __init__(self):
        self.vRed = 0
        self.vBlack = 0
        self.type = 2  #1, for alpha beta search 2,for mcts search, 3, for enhanced mcts
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
        self.HistoryTable=[0]*65536
        self.distance = 0
        self.computerMove = 0
        self.MATE_VALUE = 10000
        self.DEPTH_LIMIT = 32
        self.TIME_LIMIT = 1
        self.WIN_VALUE =  self.MATE_VALUE - 100
        

        self.calculation_time = float(5) # �������ʱ��
        self.max_actions = 400 # ÿ��ģ��Ծ������еĲ���
        self.confident = 1.96 # UCB�еĳ���
        self.plays = {} # ��¼�ŷ�����ģ��Ĵ�����������(player, move)��������ң����ӣ�
        self.wins = {} # ��¼�ŷ���ʤ�Ĵ���
        self.max_depth = 1
        self.computer_first = True

        with open("play.dat", "w+") as play:
            lines = play.readlines()
            for line in lines:
                key,value = line.split("#")
                self.plays[eval(key)] = eval(value)

        with open("win.dat", "w+") as win:
            lines = win.readlines()
            for line in lines:
                key,value = line.split("$")
                self.wins[eval(key)] = value       
        return
    def save(self):
        with open("play.dat", "w") as play:
            lines = []
            for key, value in self.plays.items():
                lines.append(str(key)+"#"+str(value)+"\n")
                play.writelines(lines)
        with open("win.dat", "w") as win:
            lines = []
            for key,value in self.wins.items():
                lines.append(str(key)+"$"+str(value)+"\n")
                win.writelines(lines)
    def __MOV(self,src,dest):
        return src+dest*256
    def GenerateMoves(self,boardPhase,movs):
        #need check if still checked here to reduce the search space
        moveCount = 0
        for src in range(256):
            chess_value = boardPhase.board_status[src]
            if(boardPhase.isSelfchess(chess_value)):
                if chess_value == 18 or chess_value == 10: #Bishop
                    for delta in Board.BiShopDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Bishop %d move: src %d, dest %d" %(chess_value,src,dest)
                elif chess_value == 9 or chess_value == 17: #Advisor
                    for delta in Board.AdvisorDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Advisor %d move: src %d, dest %d" %(chess_value,src,dest)                    
                elif chess_value == 8 or chess_value == 16: #King
                    for delta in Board.KingDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1  
                            #print "King %d move: src %d, dest %d" %(chess_value,src,dest)                 
                elif chess_value == 19 or chess_value == 11: #Knight
                    for delta in Board.KnightDeltaPin.keys():
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1
                            #print "Knight %d move: src %d, dest %d" %(chess_value,src,dest)                               
                elif chess_value == 20 or chess_value == 12: #Rook
                    for delta in Board.KingDelta:
                        dest = src+delta
                        while(Board.inBoard[dest]==1):
                            if boardPhase.isLegalMove(chess_value,src,dest):
                                movs.append(self.__MOV(src,dest))
                                moveCount = moveCount + 1
                                #print "Rook %d move: src %d, dest %d" %(chess_value,src,dest)   
                            dest = dest + delta
                elif chess_value == 21 or chess_value == 13: #Cannon
                    for delta in Board.KingDelta:
                        dest = src+delta
                        while(Board.inBoard[dest]==1):
                            if boardPhase.isLegalMove(chess_value,src,dest):
                                movs.append(self.__MOV(src,dest))
                                moveCount = moveCount + 1
                                #print "Cannon %d move: src %d, dest %d" %(chess_value,src,dest)   
                            dest = dest + delta                    
                elif chess_value == 22 or chess_value == 14: #Pawn
                    for delta in Board.KingDelta:
                        dest = src+delta
                        if boardPhase.isLegalMove(chess_value,src,dest):
                            movs.append(self.__MOV(src,dest))
                            moveCount = moveCount + 1 
                            #print "Pawn %d move: src %d, dest %d" %(chess_value,src,dest) 
        return moveCount
    def __mirrorSquare(self,index):
        return 254 - index
    def __addPiece(self,index,boardPhase,chess_value):
        boardPhase.board_status[index] =  chess_value
        if chess_value < 16:
            self.vRed = self.vRed + self.ChessValueTable[chess_value - 8][index]
        else:
            self.vBlack = self.vBlack + self.ChessValueTable[chess_value - 16][self.__mirrorSquare(index)]
    def __delPiece(self,index,boardPhase,chess_value):
        boardPhase.board_status[index] =  0
        if chess_value < 16:
            self.vRed = self.vRed - self.ChessValueTable[chess_value - 8][index]
        else:
            self.vBlack = self.vBlack - self.ChessValueTable[chess_value - 16][self.__mirrorSquare(index)]   
                 
    def move_piece(self,boardPhase,move):
        src = move%256
        dest = int(move/256)
        dest_chess_value = boardPhase.board_status[dest]
        if dest_chess_value != 0:
            self.__delPiece(dest, boardPhase, boardPhase.board_status[dest])
        self.__addPiece(dest,boardPhase,boardPhase.board_status[src]) #move the piece to new place
        self.__delPiece(src, boardPhase, boardPhase.board_status[src]) # delete the piece in the original place
        return dest_chess_value     #return the dest piece for undo move. even it has no piece in dest, it will still return 0
    
    def undo_move_piece(self,boardPhase,move,dest_chess_value):
        src = move%256
        dest = int(move/256)
        temp = boardPhase.board_status[dest]
        self.__delPiece(dest, boardPhase, temp)
        self.__addPiece(src,boardPhase,temp)
        if dest_chess_value != 0:
            self.__addPiece(dest, boardPhase, dest_chess_value)
            
    def makeMove(self,boardPhase,move):
        temp = boardPhase.board_status[move%256]
        dest_chess_value = self.move_piece(boardPhase, move)
        if boardPhase.isChecked():
            self.undo_move_piece(boardPhase, move, dest_chess_value)
            return (False,0)
        boardPhase.changeSide()
        self.distance =  self.distance + 1
        logging.info("Move chess %d, from %d to %d" %(temp,move%256,int(move/256)))
        return (True,dest_chess_value)
        
    def undoMakeMove(self,boardPhase,move,dest_chess_value):
        self.undo_move_piece(boardPhase, move,dest_chess_value)
        self.distance =  self.distance - 1
        boardPhase.changeSide()
                           
    def __alpha_beta_search(self,depth,boardPhase,alpha,beta):
        best_move = 0
        best_value = alpha
        isMated =  True
        if(depth <= 0):
            return self.__evaluate(boardPhase)
        movs = []
        movecount = self.GenerateMoves(boardPhase,movs)
        if movecount != 0:
            movs.sort(cmp=lambda x,y:cmp(self.HistoryTable[x],self.HistoryTable[y]),reverse=True)
            for move in movs:
                result = self.makeMove(boardPhase,move)
                if result[0] == True:
                    isMated = False
                    val = -self.__alpha_beta_search(depth - 1,boardPhase,-beta,-alpha)
                    self.undoMakeMove(boardPhase, move, result[1])
                    if val > beta:
                        best_value = val
                        best_move = move
                        break
                    if val >alpha:
                        alpha = val
                        best_value = val
                        best_move = move
            if isMated == True:
                return self.distance - self.MATE_VALUE
            if best_move != 0:
                self.HistoryTable[best_move] += depth * depth;
                if self.distance == 0:
                    self.computerMove = best_move
            return best_value
    def __evaluate(self,boardPhase):
        if boardPhase.getSide == 0:           
            return self.vRed - self.vBlack + 3
        else:
            return self.vBlack - self.vRed + 3
    def __mainSearch(self,boardPhase):
        start_time = time.time()
        #for i in range(self.DEPTH_LIMIT):
        #for i in range(self.DEPTH_LIMIT):
        value = self.__alpha_beta_search(2,boardPhase,-self.MATE_VALUE, self.MATE_VALUE)
        #if value > self.WIN_VALUE or value < -self.WIN_VALUE:
            #break
            #if time.time() - start_time > self.TIME_LIMIT :
            #    break

    def get_mcts_move(self, boardPhase):
        self.plays = {}
        self.wins = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            clone_boardPhase = copy.deepcopy(boardPhase)
            self.run_simulation(clone_boardPhase) # ����MCTS
            simulations += 1
        
        move = self.select_one_move(boardPhase) # ѡ������ŷ�
        self.computerMove = move

    def get_enhanced_mcts_move(self, boardPhase):
        root = TwoPlayersGameMonteCarloTreeSearchNode(state = boardPhase, parent = None)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_action(1000)
        self.computerMove = best_node

    def getBestMove(self,boardPhase):
        if self.type == 1:
            self.__mainSearch(boardPhase)
        elif self.type == 3:
            self.get_enhanced_mcts_move(boardPhase)
        else:
            self.get_mcts_move(boardPhase)
        return self.computerMove

    def select_one_move(self, boardPhase):
        movs = []
        movecount = self.GenerateMoves(boardPhase,movs)
        if movecount == 0:
            return None
        
        new_list = copy.deepcopy(movs)
        for move in new_list:
            clone = copy.deepcopy(boardPhase)
            src = move%256
            dest = int(move/256)
            value = clone.board_status[src]
            clone.board_status[src] = 0
            clone.board_status[dest] = value
            if clone.isChecked():
                movs.remove(move)
        
        if not movs:
            return None
        percent_wins, move = max(
            (self.wins.get((boardPhase.player, tuple(boardPhase.board_status), move), 0) /
             self.plays.get((boardPhase.player, tuple(boardPhase.board_status), move), 1),
             move)
            for move in movs)

        return move

    def run_simulation(self, boardPhase):
        """
        MCTS main process
        """

        plays = self.plays
        wins = self.wins

        player = boardPhase.player 
        visited_states = set()
        winner = -1
        expand = True

        # Simulation
        for t in range(1, self.max_actions + 1):
            # Selection
            
            movs = []
            movecount = self.GenerateMoves(boardPhase,movs)
            if movecount == 0:
                logging.info('win')
            
            if all(plays.get((player, tuple(boardPhase.board_status), move)) for move in movs):
                log_total = log(
                    sum(plays[(player, tuple(boardPhase.board_status), move)] for move in movs))
                value, move = max(
                    ((wins[(player, tuple(boardPhase.board_status), move)] / plays[(player, tuple(boardPhase.board_status), move)]) +
                     sqrt(self.confident * log_total / plays[(player, tuple(boardPhase.board_status), move)]), move)
                    for move in movs) 
            else:
                move = choice(movs)

            # Expand
            # only expand one step
            if expand and (player, tuple(boardPhase.board_status), move) not in plays:
                expand = False
                plays[(player, tuple(boardPhase.board_status), move)] = 0
                wins[(player, tuple(boardPhase.board_status), move)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, tuple(boardPhase.board_status), move))
            boardPhase.movePiece(move%256,move//256)

            if boardPhase.isDead(self):
                if boardPhase.getSide() == 1:
                    winner = 0
                else:
                    winner = 1
                break;

        player = boardPhase.player
        # Back-propagation
        for player, status, move in visited_states:
            if (player, status,move) not in plays:
                continue
            plays[(player, status, move)] += 1
            if player == winner:
                wins[(player, status, move)] += 1
    
    
    
    
    
    
    