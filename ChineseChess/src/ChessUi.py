#encoding: utf-8
import sys, pygame
from pygame.locals import QUIT,  MOUSEBUTTONDOWN
from ChessEngine import ChessEngine
from board_window import BoardWindow
from board_phase import *

import logging as log

   
def game_input(events,boardWindow,boardPhase,chessEngine): 
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


computer_first = False
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init() 
boardWindow = BoardWindow(computer_first)
boardPhase = MCTSBoardPhase()
#boardPhase = BoardPhase()
boardWindow.drawBoard(boardPhase)
chessEngine =  ChessEngine(3)
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
        game_input(pygame.event.get(),boardWindow,boardWindow, chessEngine)
    boardWindow.drawBoard(boardPhase)
    pygame.display.flip()

if train_flag:
    log.info('save engine param.')
    chessEngine.save()
