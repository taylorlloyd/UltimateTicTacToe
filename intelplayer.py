import operator

from  player import Player
from fractions import Fraction

class IntelPlayer(Player):
    
    wins = 1
    losses = 1
    # State = outer state, inner state, forced

    STATE_SIZE = (3 ** 90)
    MEM_SIZE = 2 ** 22
    print "Initializing learn-state memory..."
    states = [[0.0 for x in range(81)] for i in range(MEM_SIZE)]
    update_delta = 0.1
    last_mem = (0,0,0)
    last_index = 0
    print "Done"
    def getState(self, board):
        """Returns a number uniquely identifying the board state"""
        state = 0
        for i in board["array"]:
            state = (state*3) + i
        for o in board["outer"]:
            state = (state*3) + o
        #print "Board State: "+str(state)
        return state

    def getStateMem(self, state):
        mem_loc = Fraction(state*self.MEM_SIZE,self.STATE_SIZE)
        lower = int(mem_loc)
        upper = lower + 1
        #print "Memory locations: "+str(lower)+"-"+str(upper)
        
        ratio = float(mem_loc)-float(lower)

        return (lower, upper, ratio)
    
    def getStateValue(self, mem, index):
        (lower, upper, ratio) = mem
        return self.states[lower][index]*ratio + self.states[upper][index]*(1-ratio)

    def updateStateValue(self, mem, index, value):
        (lower, upper, ratio) = mem
        self.states[lower][index] = self.states[lower][index]*(1-self.update_delta*ratio) + value*self.update_delta*ratio
        self.states[upper][index] = self.states[upper][index]*(1-self.update_delta*(1-ratio)) + value*self.update_delta*(1-ratio)

    def pushOldState(self, oldmem, oldindex, newmem, newindex):
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
