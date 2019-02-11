import importlib


from Game_ct4 import Game
from MCMethod import MonteCarlo
from State_ct4 import State

game = Game()
mcts = MonteCarlo(game)

state = game.start()
winner = game.winner(state)

#Frome intial state take turns to play game until someone wins
while (winner == None):
    print("player: " + str(state.player))

    info = mcts.runSearch(state,1)
    print(info)
    stats = mcts.getStats(state)
    #print(stats)
    play = mcts.bestPlay(state)
    state = game.nextState(state, play)
    winner = game.winner(state)

print("winner: " + str(winner))