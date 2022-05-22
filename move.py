class Move:
    def __init__(self, startSquare, targetSquare, evaluation = 0):
        self.startSquare = startSquare
        self.targetSquare = targetSquare
        self.evaluation = evaluation
    
    def getStartSquare(self):
        return self.startSquare
    
    def getTargetSquare(self):
        return self.targetSquare
    
    def __gt__(self, other):
        return self.evaluation > other.evaluation
    
    def __lt__(self, other):
        return self.evaluation < other.evaluation
    
    def __le__(self, other):
        return self.evaluation <= other.evaluation
    
    def __ge__(self, other):
        return self.evaluation >= other.evaluation
    
    def __repr__(self):
        return self.evaluation.__repr__()

class PrevMove:
    def __init__(self, startSquare, targetSquare, startSquarePiece, targetSquarePiece):
        self.startSquare = startSquare
        self.targetSquare = targetSquare
        self.startSquarePiece = startSquarePiece
        self.targetSquarePiece = targetSquarePiece
    
    def getStartSquare(self):
        return self.startSquare
    
    def getTargetSquare(self):
        return self.targetSquare
    
    def getStartSquarePiece(self):
        return self.startSquarePiece
    
    def getTargetSquarePiece(self):
        return self.targetSquarePiece