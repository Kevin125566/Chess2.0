from boardUtils import BoardUtils
from move import PrevMove
from pawn import Pawn
from piece import Piece
from king import King

class GameBoard:
    def __init__(self, fenString):
        self.fenString = fenString
        self.colorToMove = fenString.getColorToMove()

        self.board = self.generateBoard()
        
        self.moveHistory = []

        self.boardUtils = BoardUtils(self.board, self.colorToMove)

        for square in range(64):
            if type(self.board[square]) == King:
                if self.board[square].getColor() == 'w':
                    self.whiteKing = self.board[square]
                else:
                    self.blackKing = self.board[square]
    
    def generateBoard(self):
        board = {}

        boardPos = 0
        for char in self.fenString.getString():
            if char.isalpha():
                if char.lower() == 'p':
                    board[boardPos] = Pawn(char, boardPos)
                elif char.lower() == 'k':
                    board[boardPos] = King(char, boardPos)
                else:
                    board[boardPos] = Piece(char, boardPos)
                boardPos += 1
            elif char.isnumeric():
                for pos in range(int(char)):
                    board[boardPos] = None
                    boardPos += 1

        return board
    
    def generateMoves(self):
        return self.boardUtils.generateMoves()

    # def generateMoves(self):
        # pseudoLegalMoves = self.generatePseudoLegalMoves()
        # legalMoves = []

        # for move in pseudoLegalMoves:
        #     startSquarePiece = self.board[move.getStartSquare()]
        #     if startSquarePiece.isPinned():
        #         print('here 2')
        #         pseudoLegalMoves.remove(move)

        # for move in pseudoLegalMoves:
        #     startSquarePiece = self.board[move.getStartSquare()]
        #     if self.colorToMove != startSquarePiece.getColor() and move.getTargetSquare() == self.whiteKing.getCurrentSquare():
        #         self.whiteKing.addToPiecesChecking(self.board[move.getStartSquare()])
        #     elif self.colorToMove != startSquarePiece.getColor() and move.getTargetSquare() == self.blackKing.getCurrentSquare():
        #         self.blackKing.addToPiecesChecking(self.board[move.getStartSquare()])
            
        # return pseudoLegalMoves
            



        # pseudoLegalMoves = self.boardUtils.generatePseudoLegalMoves()
        # legalMoves = []

        # for move in pseudoLegalMoves:
        #     startSquare = move.getStartSquare()
        #     startSquarePiece = self.board[startSquare]

        #     self.move(move)

        #     if self.colorToMove == 'w':
        #         prevColorToMove = 'b'
        #     else:
        #         prevColorToMove = 'w'

        #     opponentPseudoLegalMoves = self.boardUtils.generatePseudoLegalMoves()

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
        pass

    def move(self, move):
        startSquare = move.getStartSquare()
        targetSquare = move.getTargetSquare()

        startSquarePiece = self.board[startSquare]
        targetSquarePiece = self.board[targetSquare]

        prevMove = PrevMove(startSquare, targetSquare, startSquarePiece, targetSquarePiece)
        self.moveHistory.append(prevMove)

        startSquarePiece.increaseMovesMade()

        self.board[targetSquare] = startSquarePiece
        self.board[startSquare] = None

        startSquarePiece.setCurrentSquare(targetSquare)
        
        self.boardUtils.changeColorToMove()

    def undoMove(self):
        if len(self.moveHistory) < 1:
            return

        prevMove = self.moveHistory.pop()

        startSquare = prevMove.getStartSquare()
        targetSquare = prevMove.getTargetSquare()

        startSquarePiece = prevMove.getStartSquarePiece()
        targetSquarePiece = prevMove. getTargetSquarePiece()

        self.board[startSquare] = startSquarePiece
        self.board[targetSquare] = targetSquarePiece

        startSquarePiece.decreaseMovesMade()

        if startSquarePiece.getPiece().lower() == 'k':
            startSquarePiece.setCurrentSquare(startSquare)

        self.boardUtils.changeColorToMove()



def tests():
    pass

if __name__ == "__main__":
    tests()