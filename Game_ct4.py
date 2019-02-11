import copy
import math
from State_ct4 import State
from Play_ct4 import Play 

class Game:
    
    N_ROWS = 6
    N_COLS = 7


    boardPrototype = [ [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0] ]

    checkProtoype = [ [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0] ]


    #Generate and return the initilal game state
    def start(self):
        newBoard = copy.copy(self.boardPrototype)
        st = State([], newBoard, 1)
        return st

    def clearBoard(self):
        return copy.copy(self.boardPrototype)

    def legalPlays(self, state):
        legalplays = []
        for col in range(0, self.N_COLS):
            for row in range(0, self.N_ROWS):
                if (state.board[row][col] == 0):
                    legalplays.append(Play(row, col))
                    break

        return legalplays

    #Advance the given state and return it
    def nextState(self, state, play):
        newHistory = copy.deepcopy(state.playHistory)
        newHistory.append(play)
        newBoard = copy.deepcopy(state.board)
        newBoard[play.row][play.col] = state.player
        newPlayer = -state.player 
        
        return State(newHistory, newBoard, newPlayer)

    #Return the winner of the game
    def winner(self, state):
        if (state == None):
            print("errrror")
        thisState = state
        
        #if board is full then no winner
        
        #one board for each posisble winning orientation
        checkBoards = { 
            "h": copy.copy(self.checkProtoype),
            "v": copy.copy(self.checkProtoype),
            "l": copy.copy(self.checkProtoype),
            "r": copy.copy(self.checkProtoype)
        }
        #check horizontal
        fourinrow = 0
        for row in range(0, self.N_ROWS):
            for col in range(0, self.N_COLS):
                cell = (state.board)[row][col]
                if (abs(fourinrow + cell) > abs(fourinrow)):
                    fourinrow = fourinrow + cell
                else:
                    fourinrow = cell
                if (abs(fourinrow) == 4):
                    if (abs(fourinrow) == fourinrow):
                        return 1
                    return -1

        #check verticle
        fourinrow = 0
        for col in range(0, self.N_COLS):
            for row in range(0, self.N_ROWS):
                cell = (state.board)[row][col]
                if (abs(fourinrow + cell) > abs(fourinrow)):
                    fourinrow = fourinrow + cell
                else:
                    fourinrow = cell
                if abs(fourinrow) == 4:
                    if abs(fourinrow) == fourinrow:
                        return 1
                    return -1
     
        return None



    
    