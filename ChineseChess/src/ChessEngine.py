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
    def __init__(self, type):
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
        self.type = type  #1, for alpha beta search 2,for mcts search, 3, for enhanced mcts

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

    def __alpha_beta_search(self,depth,boardPhase,alpha,beta):
        best_move = 0
        best_value = alpha
        isMated =  True
        if(depth <= 0):
            return self.__evaluate(boardPhase)
        movs = []
        movecount, movs = boardPhase.GenerateMoves()
        if movecount != 0:
            #movs.sort(cmp=lambda x,y:cmp(self.HistoryTable[x],self.HistoryTable[y]),reverse=True)
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
        movecount, movs = boardPhase.GenerateMoves()
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
            movecount, movs = boardPhase.GenerateMoves()
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

            if boardPhase.isDead():
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
