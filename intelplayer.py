import operator

from  player import Player
from fractions import Fraction

class IntelPlayer(Player):
    
    # Win/Loss counters
    wins = 1
    losses = 1

    # State Size - The total count of possible states
    STATE_SIZE = (3 ** 90)

    # Mem Size - The number of state-action entries allocated to the system
    MEM_SIZE = 2 ** 22

    states = [[0.0 for x in range(81)] for i in range(MEM_SIZE)]
    
    # Update Delta - Quantity of change resulting from a push-back
    update_delta = 0.1

    # Tracking of previous turns
    last_mem = (0,0,0)
    last_index = 0
    
    def getState(self, board):
        """
        Returns a number uniquely identifying the board state
        
        The number must always be less than STATE_SIZE
        """
        state = 0
        for i in board["array"]:
            state = (state*3) + i
        for o in board["outer"]:
            state = (state*3) + o
        #print "Board State: "+str(state)
        return state

    def getStateMem(self, state):
        """
        Returns the indicies and ratio associated with potential actions for a given
        state. The list returned should be considered a black box except by 
        getStateValue(), updateStateValue(), and pushOldState()
        """

        mem_loc = Fraction(state*self.MEM_SIZE,self.STATE_SIZE)
        lower = int(mem_loc)
        upper = lower + 1
        #print "Memory locations: "+str(lower)+"-"+str(upper)
        
        ratio = float(mem_loc)-float(lower)

        return (lower, upper, ratio)
    
    def getStateValue(self, mem, index):
        """
        Returns a float representing the relative value of the action indicated by index.
        Higher is better, but no range of potential values is guaranteed.
        """

        (lower, upper, ratio) = mem
        return self.states[lower][index]*ratio + self.states[upper][index]*(1-ratio)

    def updateStateValue(self, mem, index, value):
        """
        Updates the value associated with the state indicated by `mem` and index.
        Utilizes update_delta to determine how much change to make
        """

        (lower, upper, ratio) = mem
        self.states[lower][index] = self.states[lower][index]*(1-self.update_delta*ratio) + value*self.update_delta*ratio
        self.states[upper][index] = self.states[upper][index]*(1-self.update_delta*(1-ratio)) + value*self.update_delta*(1-ratio)

    def pushOldState(self, oldmem, oldindex, newmem, newindex):
        """
        Updates the value indicated by oldmem, old index by taking into account the value
        of newmem, nemindex.
        """

        (lower, upper, ratio) = newmem
        self.updateStateValue(oldmem, oldindex, self.getStateValue(newmem, newindex))

    def notifyWin(self):
        self.updateStateValue(self.last_mem, self.last_index, 1)
        self.wins += 1
        print float(self.wins) / float(self.losses)

    def notifyLose(self):
        self.updateStateValue(self.last_mem, self.last_index, -1)
        self.losses += 1
        print float(self.wins) / float(self.losses)

    def playTurn(self, board):
        state = self.getState(board)
        values = self.getStateMem(state)

        options = []
        for i in range(81):
            if((board["forced"] == 9 or i/9 == board["forced"]) and board["array"][i] == 0):
                options.append((i, self.getStateValue(values, i)))

        choice = max(options, key=operator.itemgetter(1)) 

        #print "Choosing "+str(choice[0])+", Value: "+str(choice[1])

        self.pushOldState(self.last_mem, self.last_index, values, choice[0])

        self.last_mem = values
        self.last_index = choice[0]
        return choice[0]
