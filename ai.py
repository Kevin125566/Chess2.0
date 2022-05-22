from evaluation import Evaluation
import random
import time

class Ai:
    def __init__(self, colorToPlay, gameBoard):
        self.colorToPlay = colorToPlay
        self.gameBoard = gameBoard
        self.moveCache = {}
    
    def getMoves(self):
        legalMoves = self.gameBoard.generateMoves()

        return legalMoves

    def makeRandomMove(self):
        legalMoves = self.getMoves()

        if len(legalMoves) > 0:
            randomMove = random.choice(legalMoves)

            time.sleep(0.1)
            self.gameBoard.move(randomMove)

            return randomMove
        else:
            print("Checkmate")
    
    def makeNegamaxMove(self):
        legalMoves = self.gameBoard.generateMoves()

        self.moveOrdering(legalMoves)

        depth = 1

        if len(legalMoves) < 1:
            return

        values = []
        for move in legalMoves:
            value = self.negamax(move, depth, -9999, 9999, 1)
            values.append(value)
        
        print(values)
        
        indices = []
        maxValue = values[0]
        for i in range(len(values)):
            if values[i] > maxValue:
                maxValue = values[i]
        
        for j in range(len(values)):
            if maxValue == values[j]:
                indices.append(j)
        
        movesToMake = []
        for k in indices:
            movesToMake.append(legalMoves[k])

        moveToMake = random.choice(movesToMake)
        self.gameBoard.move(moveToMake)
        return moveToMake
    
    def makeMinimaxMove(self, maximizingPlayer):
        legalMoves = self.gameBoard.generateMoves()

        self.moveOrdering(legalMoves, maximizingPlayer)

        depth = 3

        if len(legalMoves) < 1:
            return

        startTime = time.time()
        values = []
        for move in legalMoves:
            value = self.minimax(move, depth, -99999, 99999, maximizingPlayer)
            values.append(value)
        
        print(values)
        
        indices = []
        maxValue = values[0]
        for i in range(len(values)):
            # if maximizingPlayer and values[i] > maxValue:
            #     maxValue = values[i]
            if values[i] < maxValue:
                maxValue = values[i]
        
        for j in range(len(values)):
            if maxValue == values[j]:
                indices.append(j)
        
        movesToMake = []
        for k in indices:
            movesToMake.append(legalMoves[k])
        
        endTime = time.time()

        print(endTime - startTime)

        moveToMake = random.choice(movesToMake)
        self.gameBoard.move(moveToMake)
        return moveToMake
    
    def negamax(self, move, depth, alpha, beta, color):
        self.gameBoard.move(move)

        if depth == 0:
            evaluation = Evaluation(self.gameBoard)
            score = evaluation.evaluatePos()
            self.gameBoard.undoMove()
            return score

        legalMoves = self.gameBoard.generateMoves()

        self.moveOrdering(legalMoves)

        value = -99999
        for move in legalMoves:
            value = max(value, self.negamax(move, depth - 1, -beta, -alpha, -color))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        self.gameBoard.undoMove()

        return value
    
    def minimax(self, move, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            evaluation = Evaluation(self.gameBoard.board)
            score = evaluation.evaluatePos(self.gameBoard.board)
            return score
        
        self.gameBoard.move(move)

        currentState = (tuple(self.gameBoard.board.items()), depth, maximizingPlayer)

        if currentState in self.moveCache:
            self.gameBoard.undoMove()
            return self.moveCache[currentState]

        opponentMoves = self.gameBoard.generateMoves()
        self.moveOrdering(opponentMoves, maximizingPlayer)
        if maximizingPlayer:
            value = -9999
            for move in opponentMoves:
                value = max(value, self.minimax(move, depth - 1, alpha, beta, False))
                if beta <= alpha:
                    break
                alpha = max(alpha, value)
            self.moveCache[(tuple(self.gameBoard.board.items()), depth, maximizingPlayer)] = value
            self.gameBoard.undoMove()
            return value
        else:
            value = 9999
            for move in opponentMoves:
                value = min(value, self.minimax(move, depth - 1, alpha, beta, True))
                if beta <= alpha:
                    break
                beta = min(beta, value)
            self.moveCache[(tuple(self.gameBoard.board.items()), depth, maximizingPlayer)] = value
            self.gameBoard.undoMove()
            return value
    
    def moveOrdering(self, moves, maximizingPlayer):
        self.quickSort(moves, 0, len(moves) - 1, maximizingPlayer)

    def partition(self, array, low, high, maximizingPlayer):
        pivot = array[high]

        i = low - 1

        if maximizingPlayer:
            for j in range(low, high):
                if array[j] >= pivot:
                    i += 1

                    (array[i], array[j]) = (array[j], array[i])

            (array[i + 1], array[high]) = (array[high], array[i + 1])
        else:
            for j in range(low, high):
                if array[j] <= pivot:
                    i += 1

                    (array[i], array[j]) = (array[j], array[i])

            (array[i + 1], array[high]) = (array[high], array[i + 1])

        
        return i + 1
    
    def quickSort(self, array, low, high, maximizingPlayer):
        if low < high:

            pi = self.partition(array, low, high, maximizingPlayer)

            self.quickSort(array, low, pi - 1, maximizingPlayer)
            self.quickSort(array, pi + 1, high, maximizingPlayer)

    
    def getColorToPlay(self):
        return self.colorToPlay
    

class State:
    def __init__(self, board, depth, player):
        self.board = board
        self.depth = depth
        self.player = player
    
