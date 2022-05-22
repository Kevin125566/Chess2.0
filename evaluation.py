class Evaluation:
    def __init__(self, boardPos):
        self.boardPos = boardPos
        self.evaluationScore = self.evaluatePos(self.boardPos)
    
    def evaluatePos(self, boardPos):
        wK = 0
        wKPsn = 0
        bK = 0
        bKPsn = 0
        wN = 0
        wNPsn = 0
        bN = 0
        bNPsn = 0
        wB = 0
        bB = 0
        wQ = 0
        bQ = 0
        wR = 0
        bR = 0
        wP = 0
        bP = 0 

        for square in range(64):
            pieceOnSquare = boardPos[square]
            if pieceOnSquare != None:
                piece = pieceOnSquare.getPiece()
                if piece == 'K':
                    wK += 1
                    if piece in range(48, 64):
                        wKPsn += 5
                elif piece == 'k':
                    bK += 1
                    if piece in range(0, 16):
                        bKPsn += 5
                elif piece == 'N':
                    wN += 1
                    if pieceOnSquare.getCurrentSquare() in (18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 43, 44, 45, 46):
                        wNPsn += 5
                elif piece == 'n':
                    bN += 1
                    if pieceOnSquare.getCurrentSquare() in (18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 43, 44, 45, 46):
                        bNPsn += 5
                elif piece == 'B':
                    wB += 1
                elif piece == 'b':
                    bB += 1
                elif piece == 'Q':
                    wQ += 1
                elif piece == 'q':
                    bQ += 1
                elif piece == 'R':
                    wR += 1
                elif piece == 'r':
                    bR += 1
                elif piece == 'P':
                    wP += 1
                elif piece == 'p':
                    bP += 1
        
        materialScore = 900 * (wK - bK) + 90 * (wQ - bQ) + 50 * (wR - bR) + 30 * (wN - bN) + 30 * (wB - bB) + 10 * (wP - bP)

        piecePsnScore = 100 * (wKPsn - bKPsn) + 30 * (wNPsn - bNPsn)

        return materialScore + piecePsnScore

    def evaluateMove(self, move):
        startSquare = move.getStartSquare()
        targetSquare = move.getTargetSquare()
        startSquarePiece = self.boardPos[startSquare]
        
        newBoard = self.boardPos.copy()

        newBoard[startSquare] = None
        newBoard[targetSquare] = startSquarePiece

        score = self.evaluatePos(newBoard)
        return score

    
    def __le__(self, other):
        return self.evaluationScore <= other.evaluationScore
    
    def __ge__(self, other):
        return self.evaluationScore >= other.evaluationScore
    
    def __repr__(self):
        return str(self.evaluationScore)