from piece import Piece

class Pawn(Piece):
    def __init__(self, piece, currentSquare):
        super().__init__(piece, currentSquare)
    
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
        return super().getCurrentSquare()
    
    def setCurrentSquare(self, newSquare):
        return super().setCurrentSquare(newSquare)
    
    def addPiecePinning(self, pieceToAdd):
        return super().addPiecePinning(pieceToAdd)
    
    def removePins(self):
        return super().removePins()
    
    def isPinned(self):
        return super().isPinned()

    def checkEnPassant(self):
        if self.movesMade == 0:
            return True
        else:
            return False