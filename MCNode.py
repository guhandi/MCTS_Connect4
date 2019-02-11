import math

class MonteCarloNode:
    
    def __init__(self, parent, play, state, unexpandedPlays):
        self.play = play
        self.state = state

        #Monte Carlo stuff
        self.n_plays = 0
        self.n_wins = 0

        #Tree stuff
        self.parent = parent
        self.children = {}

        for play in unexpandedPlays:
            #MonteCarloNode.children is a map from play hashes to an object containing 
            #(1) the play object and (2) the associated child node
            self.children[play.hash()] = {play:None}

    #Get the MonteCarloNode corresponding to the given play
    def childNode(self, play):
        child = self.children.get(play.hash())
        if (child == None):
            raise ValueError('Child is not expanded')
        
        return child.get(play)

    #Expand the specified child play and return the new child node.
    #Add the node to the array of children nodes.
    #Remove the play from the array of unexpanded plays.
    #@param {Play} play - The play to expand.
    #@param {State} childState - The child state corresponding to the given play.
    #@param {Play[]} unexpandedPlays - The given child's unexpanded child plays; typically all of them.
    #@return {MonteCarloNode} The new child node.
    def expand(self, play, childState, unexpandedPlays):
        invalid = self.children[play.hash()] == None
        if (invalid):
            raise ValueError('No such play!')
        childNode = MonteCarloNode(self, play, childState, unexpandedPlays)
        self.children[play.hash()] = {play: childNode}
        #self.children[play.hash()].update({play: childNode})
        #if (self.state.hash() == str([])):
        #    print(childNode)
        #    print(self.children)

        return childNode

    #Get all legal plays from this node
    def allPlays(self):
        ret = []
        for key, child in self.children.iteritems():
            for play, node in child.iteritems():
                ret.append(play)
                
        
        return ret

    #Get all unexpanded legal plays from this node
    def unexpandedPlays(self):
        ret = []
        for key, child in self.children.iteritems():
            for play, node in child.iteritems():
                if (node == None):
                    ret.append(play)
        
        return ret

    #Whether this node is fully expanded
    def isFullyExpanded(self):
        #print(self.children)
        for key, child in self.children.iteritems():
            for play, node in child.iteritems():
            #child = dictionary from play key. Value of child is node
                if (node == None):
                    return False

        return True

    #Whether this node is terminal in the game tree, NOT INCLUSIVE of termination due to winning
    def isLeaf(self):
        if (len(self.children) == 0):
            return True
        return False

    #Get the UCB1 value for this node
    def getUCB1(self, biasParam):
        val = (self.n_wins/self.n_plays) + math.sqrt(biasParam * math.log(self.parent.n_plays) / self.n_plays)
        return val

    def getNode(self):
        return self

    def check(self):
        print("hfjahsdlfhaiudsfhiuasdhfiashdf")
