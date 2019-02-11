import time
import math
import random
import copy

from MCNode import MonteCarloNode
from Play_ct4 import Play
from State_ct4 import State


#class representing the Monte Carlo method
class MonteCarlo:

    def __init__(self, game, UCB1ExploreParam = 2):
        self.game = game
        self.UCB1ExploreParam = UCB1ExploreParam
        self.nodes = {}

    #If given state does not exist, create dangling node
    def makeNode(self, state):
        if (not(state.hash() in self.nodes)):
            unexpandedPlays = copy.copy(self.game.legalPlays(state))
            #for p in unexpandedPlays:
            #    print(p.seePlays())
            node = MonteCarloNode(None, None, state, unexpandedPlays)
            self.nodes.update({state.hash() : node})
        
            

    #From given state, repeatedly run MCTS to build statistics
    def runSearch(self, state, timeout = 2):
        #gamestate = copy.deepcopy(state)
        self.makeNode(state)
        #print(state.board)
        draws = 0
        totalSims = 0
        end = time.time() + timeout*10
        test=30
        tt=0

        while (time.time() < end):
         
            node  = self.select(state)
            winner = self.game.winner(node.state)
            
            
            if ((node.isLeaf() == False) & (winner == None)):
                node = self.expand(node)
                winner = self.simulate(node)

            #print(winner)
            #print(totalSims)
            
            self.backpropogate(node, winner)

            if (winner == 0):
                draws = draws + 1
            
            totalSims = totalSims + 1

        return {'runtime' : timeout, 'simulations' : totalSims, 'draws' : draws}
    

    #Phase 1, Selection: Select until not fully expanded OR leaf
    def select(self, state):
        
        bestPlay = Play(-1,-1)
        node = self.nodes.get(state.hash())
        #print(self.nodes)

        plays = node.allPlays()
        
        while (node.isFullyExpanded() & (not node.isLeaf())):
            plays = node.allPlays()
            bestUCB1 = -10000000000 #-infinity
            for play in plays:
                childUCB1 = node.childNode(play).getUCB1(self.UCB1ExploreParam)
                #print(childUCB1)
                if (childUCB1 > bestUCB1):
                    bestPlay = play
                    bestUCB1 = childUCB1

            node = node.childNode(bestPlay)
            
        return node

    #Phase 2, Expansion: Expand a random unexpanded child node
    def expand(self, node):
        
        plays = node.unexpandedPlays()
        index = random.randint(0,len(plays)-1)
        play = plays[index]

        childState = self.game.nextState(node.state, play)
        childUnexpandedPlays = self.game.legalPlays(childState)
        childNode = node.expand(play, childState, childUnexpandedPlays)
        self.nodes.update({childState.hash(): childNode})
        
        if (node.state.hash() == str([])):
            #print(node.state.hash())
            #print(childNode.children)
            idx = False

        return childNode

    #Phase 3, Simulation: Play game to terminal state, return winner
    def simulate(self, node):
        #state = copy.deepcopy(node.state)
        state = node.state
        winner = self.game.winner(state)
        while (winner == None):
            plays = self.game.legalPlays(state)
            if (len(plays) == 0):
                winner=0
                break
            play = plays[random.randint(0, len(plays)-1)]
            state = self.game.nextState(state, play)
            winner = self.game.winner(state)
        
        return winner

    #Phase 4, Backpropagation: Update ancestor statistics
    def backpropogate(self, node, winner):
        while (node != None):
            node.n_plays += 1
            # Parent's choice        
            if (node.state.isPlayer(winner)):
                node.n_wins += 1

            node = node.parent

        #module.exports = MonteCarlo
        

    #Get the best move from available statistics
    def bestPlay(self, state):
        self.makeNode(state)
        
        #If not all children are expanded, not enough info
        currnode = self.nodes.get(state.hash())

        if (currnode.isFullyExpanded() == False):
            raise ValueError('Not enough information')

        node = self.nodes.get(state.hash())
        allPlays = node.allPlays()
        maxval = -100000000

        for play in allPlays:
            childNode = node.childNode(play)
            if (childNode.n_plays > maxval):
                bestPlay = play
                maxval = childNode.n_plays

        return bestPlay

    # Return MCTS statistics for this node and children nodes
    def getStats(self, state):
        node = self.nodes.get(state.hash())
        stats = { 'n_plays': node.n_plays, 'n_wins': node.n_wins, 'children': [] }
        for key, child in node.children.iteritems():
            for cplay, cnode in child.iteritems():
                if (cnode == None):
                    stats.get('children').append({Play : cplay, 'n_plays' : None, 'n_wins' :None})
                else:
                    stats.get('children').append({Play : cplay, 'n_plays' : cnode.n_plays, 'n_wins' : cnode.n_wins})
        
        return stats

    
    
