from fractions import Fraction

class IntelPlayer(Player):

    # State = outer state, inner state, forced

    STATE_SIZE = (3 ** 90) * 10
    MEM_SIZE = 2 ** 20
    states = [0.0 for i in range(MEM_SIZE)]

    def getState(self, board):
        """Returns a number uniquely identifying the board state"""
        state = board["forced"]
        for o in board["outer"]:
            state = (state*3) + o
        for i in board["array"]:
            state = (state*3) + i
        print "Board State: "+str(state)
        return state

    def getStateValue(self, state):
        mem_loc = Fraction(state*self.MEM_SIZE,self.STATE_SIZE)
        lower = int(mem_loc)
        upper = lower + 1
        print "Memory locations: "+str(lower)+"-"+str(upper)
        
        
