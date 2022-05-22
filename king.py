from piece import Piece

class King(Piece):
    def __init__(self, piece, currentSquare):
        super().__init__(piece,currentSquare)
        self.piecesChecking = []
    
    def getValue(self):
        return super().getValue()
    
    def getColor(self):
        return super().getColor()

    def getPiece(self):
        return super().getPiece()

    def getMovesMade(self):
        return super().getMovesMade()
    
    def increaseMovesMade(self):
        return super().increaseMovesMade()
    
    def decreaseMovesMade(self):
        return super().decreaseMovesMade()
    
    def getCurrentSquare(self):
        return self.currentSquare
    
    def setCurrentSquare(self, newSquare):
        self.currentSquare = newSquare
    
    def addToPiecesChecking(self, pieceToAdd):
        if pieceToAdd not in self.piecesChecking:
            self.piecesChecking.append(pieceToAdd)
    
    def removeFromPiecesChecking(self, pieceToRemove):
        if pieceToRemove in self.piecesChecking:
            self.piecesChecking.remove(pieceToRemove)