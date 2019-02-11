import json
import numpy as np

class State:

    def __init__(self, playHistory, board, player):
        self.playHistory = playHistory
        self.board = board
        self.player = player

    def isPlayer(self, player):
        return (player == self.player)

    def getBoard(self):
        return self.board

    def hash(self):
        #return str(self.board)
        return str(self.playHistory)


