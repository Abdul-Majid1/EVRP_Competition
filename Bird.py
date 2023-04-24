class bird:
    def __init__(self, velocity, pBest,  lbest, position,pbest_value):
        self.velocity =  velocity
        self.position = position
        self.pBest = pBest
        self.pBest_value= pbest_value
        self.lbest = lbest
        self.found= False 
        self.kitna =0