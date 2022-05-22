class Piece:
    def __init__(self, piece, currentSquare):
        self.piece = piece
        self.movesMade = 0
        self.value = self.getValue()
        self.currentSquare = currentSquare
        self.piecesPinning = []

    def getValue(self):
        pieceValues = {"p": -10, "n": -30, "b": -30, "r": -50, "q": -90, "k": -900, "P": 10, "N": 30, "B": 30, "R": 50, "Q": 90, "K": 900}

        return pieceValues[self.piece]
    
    def getColor(self):
        if self.piece.islower():
            return 'b'
        else:
            return 'w'
    
    def getPiece(self):
        return self.piece
    
    def getMovesMade(self):
        return self.movesMade
    
    def increaseMovesMade(self):
        self.movesMade += 1
    
    def decreaseMovesMade(self):
        if self.movesMade > 0:
            self.movesMade -= 1
    
    def getCurrentSquare(self):
        return self.currentSquare
    
    def setCurrentSquare(self, newSquare):
        self.currentSquare = newSquare
    
    def addPiecePinning(self, pieceToAdd):
        self.piecesPinning.append(pieceToAdd)
    
    def removePins(self):
        self.piecesPinning = []
    
    def isPinned(self):
        return len(self.piecesPinning) != 0

    def getFile(self):
        pass

    def getRank(self):
        pass

def tests():
    wbishop = Piece("B")
    bbishop = Piece("b")
    
    wpawn = Piece("P")
    bpawn = Piece("p")

    wknight = Piece("N")
    bknight = Piece("n")

    wrook = Piece("R")
    brook = Piece("r")

    wqueen = Piece("Q")
    bqueen = Piece("q")

    wking = Piece("K")
    bking = Piece("k")

    print(wbishop.value, bbishop.value, wpawn.value, bpawn.value, wknight.value, bknight.value,
    wrook.value, brook.value, wqueen.value, bqueen.value, wking.value, bking.value)

if __name__ == "__main__":
    tests()

