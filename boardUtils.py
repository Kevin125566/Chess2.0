from evaluation import Evaluation
from move import Move

class BoardUtils:
    def __init__(self, board, colorToMove):
        self.board = board
        self.colorToMove = colorToMove

        self.numSquaresToEdge = self.computeSquaresToEdge()
    
    def generateMoves(self):
        pseudoLegalMoves = self.generatePseudoLegalMoves()
        illegalMoves = []

        for move in pseudoLegalMoves:
            startSquarePiece = self.board[move.getStartSquare()]
            if startSquarePiece.isPinned():
                illegalMoves.append(move)
        
        legalMoves = [x for x in pseudoLegalMoves if x not in illegalMoves]

        # for move in pseudoLegalMoves:
        #     startSquarePiece = self.board[move.getStartSquare()]
        #     if self.colorToMove != startSquarePiece.getColor() and move.getTargetSquare() == self.whiteKing.getCurrentSquare():
        #         self.whiteKing.addToPiecesChecking(self.board[move.getStartSquare()])
        #     elif self.colorToMove != startSquarePiece.getColor() and move.getTargetSquare() == self.blackKing.getCurrentSquare():
        #         self.blackKing.addToPiecesChecking(self.board[move.getStartSquare()])
        
        return legalMoves
            



        # pseudoLegalMoves = self.generatePseudoLegalMoves()
        # legalMoves = []

        # for move in pseudoLegalMoves:
        #     startSquare = move.getStartSquare()
        #     startSquarePiece = self.board[startSquare]

        #     self.move(move)

        #     if self.colorToMove == 'w':
        #         prevColorToMove = 'b'
        #     else:
        #         prevColorToMove = 'w'

        #     opponentPseudoLegalMoves = self.generatePseudoLegalMoves()

        #     goodMove = True
        #     for opponentMove in opponentPseudoLegalMoves:
        #         startSquare = opponentMove.getStartSquare()
        #         targetSquare = opponentMove.getTargetSquare()
        #         startSquarePiece = self.board[startSquare]
                
        #         if startSquarePiece.getColor() != prevColorToMove:
        #             if prevColorToMove == 'w':
        #                 if targetSquare == self.whiteKing.getCurrentSquare():
        #                     goodMove = False
        #                     break
        #             else:
        #                 if targetSquare == self.blackKing.getCurrentSquare():
        #                     goodMove = False
        #                     break
            
        #     if goodMove:
        #         legalMoves.append(move)
            
        #     self.undoMove()

        #     #TODO: remove this and fix up code
        #     for move in legalMoves:
        #         if self.board[move.getStartSquare()] == None:
        #             legalMoves.remove(move)
        
        # return legalMoves
        # return pseudoLegalMoves
        pass
   
    def generatePseudoLegalMoves(self):
        pseudoLegalMoves = []
        slidingPieces = ('b', 'q', 'r')

        for startSquare in range(64):
            piece = self.board[startSquare]
            
            if piece != None and piece.getColor() == self.colorToMove:
                # remove all pieces that are pinning this piece
                #piece.removePins()

                if piece.getPiece().lower() in slidingPieces:
                    self.generateSlidingMoves(startSquare, piece, pseudoLegalMoves)
                elif piece.getPiece().lower() == "n":
                    self.generateKnightMoves(startSquare, piece, pseudoLegalMoves)
                elif piece.getPiece().lower() == "p":
                    self.generatePawnMoves(startSquare, piece, pseudoLegalMoves)
                elif piece.getPiece().lower() == "k":
                    self.generateKingMoves(startSquare, piece, pseudoLegalMoves)
        
        return pseudoLegalMoves
    
    def generateSlidingMoves(self, startSquare, piece, moves):
        directionOffsets = [-8, 8, -1, 1, -9, 7, -7, 9]

        if piece.getPiece().lower() == 'b':
            startIndex = 4
        else:
            startIndex = 0

        if piece.getPiece().lower() == 'r':
            endIndex = 4
        else:
            endIndex = 8

        for directionIndex in range(startIndex, endIndex):
            for i in range(self.numSquaresToEdge[startSquare][directionIndex]):
                targetSquare = startSquare + directionOffsets[directionIndex] * (i + 1)
                pieceOnSquare = self.board[targetSquare]

                # Friendly piece encountered
                if pieceOnSquare != None and pieceOnSquare.getColor() == piece.getColor():
                    break

                evaluation = Evaluation(self.board)
                score = evaluation.evaluateMove(Move(startSquare, targetSquare))
                
                newMove = Move(startSquare, targetSquare, score)
                moves.append(newMove)

                # Opponent piece encountered and checking for the piece is pinned
                if pieceOnSquare != None and pieceOnSquare.getColor() != piece.getColor():
                    for remainingSquares in range(i + 1, self.numSquaresToEdge[startSquare][directionIndex]):
                        kingSquare = startSquare + directionOffsets[directionIndex] * (remainingSquares + 1)
                        kingOnSquare = self.board[kingSquare]

                        if kingOnSquare != None:
                            if kingOnSquare.getPiece().lower() == 'k' and kingOnSquare.getColor() != piece.getColor():
                                pieceOnSquare.addPiecePinning(piece)
                            break
                    break
    
    def generateKnightMoves(self, startSquare, piece, moves):
        knightOffsets = [-17, -15, -10, -6, 6, 10, 15, 17]
        sideFiles = [(0, 8, 16, 24, 32, 40, 48, 56), (1, 9, 17, 25, 33, 41, 49, 57), (6, 14, 22, 30, 38, 46, 54, 62), (7, 15, 23, 31, 39, 47, 55, 63)]

        for knightMoveIndex in range(len(knightOffsets)):
            targetSquare = startSquare + knightOffsets[knightMoveIndex]
            if targetSquare < 64 and targetSquare >= 0:
                
                # Avoiding wrap arounds
                if startSquare in sideFiles[0] and (knightMoveIndex == 0 or knightMoveIndex == 2 or knightMoveIndex == 4 or knightMoveIndex == 6):
                    continue
                elif startSquare in sideFiles[1] and (knightMoveIndex == 2 or knightMoveIndex == 4):
                    continue
                elif startSquare in sideFiles[2] and (knightMoveIndex == 3 or knightMoveIndex == 5):
                    continue
                elif startSquare in sideFiles[3] and (knightMoveIndex == 1 or knightMoveIndex == 3 or knightMoveIndex == 5 or knightMoveIndex == 7):
                    continue

                pieceOnSquare = self.board[targetSquare]

                # Friendly Piece encountered
                if pieceOnSquare != None and pieceOnSquare.getColor() == piece.getColor():
                    continue

                evaluation = Evaluation(self.board)
                score = evaluation.evaluateMove(Move(startSquare, targetSquare))
                
                newMove = Move(startSquare, targetSquare, score)
                moves.append(newMove)

    def generatePawnMoves(self, startSquare, piece, moves):
        pawnOffsets = [-8, 8, -9, 7, -7, 9]

        if piece.getColor() == 'w':
            startIndex = 0
            endIndex = 6
        else:
            startIndex = 1
            endIndex = 6

        for pawnMoveIndex in range(startIndex, endIndex, 2):

            if pawnMoveIndex == startIndex:
                for i in range(self.numSquaresToEdge[startSquare][pawnMoveIndex]):
                    targetSquare = startSquare + pawnOffsets[pawnMoveIndex] * (i + 1)
                    pieceOnSquare = self.board[targetSquare]

                    if pieceOnSquare == None and i < 1:
                        evaluation = Evaluation(self.board)
                        score = evaluation.evaluateMove(Move(startSquare, targetSquare))
                
                        newMove = Move(startSquare, targetSquare, score)
                        moves.append(newMove)
                        continue
                    
                    if pieceOnSquare == None and piece.getMovesMade() == 0:
                        evaluation = Evaluation(self.board)
                        score = evaluation.evaluateMove(Move(startSquare, targetSquare))
                
                        newMove = Move(startSquare, targetSquare, score)
                        moves.append(newMove)
                    
                    break

            else:
                for i in range(self.numSquaresToEdge[startSquare][pawnMoveIndex + 2]):
                    targetSquare = startSquare + pawnOffsets[pawnMoveIndex]
                    pieceOnSquare = self.board[targetSquare]

                    if pieceOnSquare != None and pieceOnSquare.getColor() != piece.getColor():
                        evaluation = Evaluation(self.board)
                        score = evaluation.evaluateMove(Move(startSquare, targetSquare))
                
                        newMove = Move(startSquare, targetSquare, score)
                        moves.append(newMove)
                        
                    break

    def pawnPromotion(self):
        pass

    def generateKingMoves(self, startSquare, piece, moves):
        directionOffsets = [-8, 8, -1, 1, -9, 7, -7, 9]

        for directionIndex in range(8):
            for i in range(self.numSquaresToEdge[startSquare][directionIndex]):
                targetSquare = startSquare + directionOffsets[directionIndex] * (i + 1)
                pieceOnSquare = self.board[targetSquare]

                # Friendly piece encountered
                if pieceOnSquare != None and pieceOnSquare.getColor() == piece.getColor():
                    break

                evaluation = Evaluation(self.board)
                score = evaluation.evaluateMove(Move(startSquare, targetSquare))
                
                newMove = Move(startSquare, targetSquare, score)
                moves.append(newMove)

                # Opponent piece encountered
                if pieceOnSquare != None and pieceOnSquare.getColor() != piece.getColor():
                    break
            
                break
        
        # Castling
    
    def changeColorToMove(self):
        if self.colorToMove == 'w':
            self.colorToMove = 'b'
        else:
            self.colorToMove = 'w'


    def computeSquaresToEdge(self):
        numSquaresToEdge = {}

        for file in range(8):
            for rank in range(8):
                squaresToNorth = rank
                squaresToSouth = 7 - rank
                squaresToEast = 7 - file
                squaresToWest = file

                squareIndex = rank * 8 + file

                numSquaresToEdge[squareIndex] = (
                    squaresToNorth,
                    squaresToSouth,
                    squaresToWest,
                    squaresToEast,
                    # Diagonals
                    min(squaresToNorth, squaresToWest),  # NW
                    min(squaresToSouth, squaresToWest),  # SW
                    min(squaresToNorth, squaresToEast),  # NE
                    min(squaresToSouth, squaresToEast)   # SE

                )
        
        return numSquaresToEdge

