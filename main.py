from tkinter import Y
from board import GameBoard
from ai import Ai
import pygame

# TODO: we dont really need to make an undo in the main where images are updated because undoing would really only happen in the game board, we can update images
# only when we make a valid move. Have the game board return true of false or something like that when checking for legal moves

def main():
    pygame.init()
    pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Chess")
    wSurface = pygame.display.get_surface()
    game = Game(wSurface)
    game.play()
    pygame.quit()

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.bgColor = pygame.Color("black")

        self.debounce = False

        self.FPS = 60
        self.closeClicked = False
        self.continueGame = True

        self.imageTileGroup = pygame.sprite.Group()
        self.imagePieceGroup = pygame.sprite.Group()

        self.imageBoard = []
        self.createBoard()

        self.fenString = FenString()
        self.colorToMove = self.fenString.getColorToMove()

        self.generatePieceImages()

        self.gameBoard = GameBoard(self.fenString)
        self.moveHistory = []

        self.draggingPiece = False
        self.imagePieceDragged = None
        self.prevImageTile = None

        self.ai = Ai('b', self.gameBoard)
        self.ai2 = Ai('w', self.gameBoard)

    def createBoard(self):
        width = self.surface.get_width() // 8
        height = self.surface.get_height() // 8

        temp = 1
        tileNumber = 0
        for rowIndex in range(8):
            row = []
            for colIndex in range(8):
                x = colIndex * width
                y = rowIndex * height
                if temp % 2 == 0:
                    color = '#769656'
                else:
                    color = '#eeeed2'
                imageTile = ImageTile(width, height, x, y, color, self.surface, tileNumber)
                self.imageTileGroup.add(imageTile)
                row.append(imageTile)
                temp += 1
                tileNumber += 1
            self.imageBoard.append(row)
            temp += 1
    
    def play(self):
        while not self.closeClicked:
            self.handleEvents()
            self.draw()
            # if self.continueGame and self.colorToMove == self.ai.getColorToPlay():
            #     moveMade = self.ai.makeMinimaxMove(True)
            #     self.updateImages(moveMade)
            #     if self.colorToMove == 'w':
            #         self.colorToMove = 'b'
            #     else:
            #         self.colorToMove = 'w'
            # elif self.continueGame and self.colorToMove == self.ai2.getColorToPlay():
            #     moveMade = self.ai.makeMinimaxMove(True)
            #     self.updateImages(moveMade)
            #     if self.colorToMove == 'w':
            #         self.colorToMove = 'b'
            #     else:
            #         self.colorToMove = 'w'
    
    def updateImages(self, moveMade):
        startSquare = moveMade.getStartSquare()
        targetSquare = moveMade.getTargetSquare()

        for imageTile in self.imageTileGroup:
            if startSquare == imageTile.getTileNumber():
                firstTile = imageTile
                break
        
        for imageTile in self.imageTileGroup:
            if targetSquare == imageTile.getTileNumber():
                secondTile = imageTile
                break
        
        secondTile.setImagePiece(firstTile.getImagePiece(), self.imagePieceGroup)
        firstTile.getImagePiece().placeDown(secondTile.getCoords())
        firstTile.setImagePiece(None)


        
    def generatePieceImages(self):
        images = {"r": "./images/Chess_rdt60.bmp", "n": "./images/Chess_ndt60.bmp", "k": "./images/Chess_kdt60.bmp", "p": "./images/Chess_pdt60.bmp",
        "b": "./images/Chess_bdt60.bmp", "q": "./images/Chess_qdt60.bmp", "R": "./images/Chess_rlt60.bmp", "N": "./images/Chess_nlt60.bmp", 
        "K": "./images/Chess_klt60.bmp", "P": "./images/Chess_plt60.bmp", "B": "./images/Chess_blt60.bmp", "Q": "./images/Chess_qlt60.bmp"}

        x = 0
        y = 0
        for char in self.fenString.getString():
            if char.isalpha():
                imagePiece = ImagePiece(images[char], self.imageBoard[x][y], self.surface)
                self.imagePieceGroup.add(imagePiece)
                self.imageBoard[x][y].setInitImagePiece(imagePiece)
                y += 1
            elif char.isnumeric():
                y += int(char)
            else:
                y = 0
                x += 1
            
    
    def draw(self):
        self.surface.fill(self.bgColor)

        self.imageTileGroup.draw(self.surface)
        self.imagePieceGroup.draw(self.surface)
        pygame.display.update()
        
    
    def handleEvents(self):
        events = pygame.event.get()

        for event in events:
            mousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.closeClicked = True

            elif event.type == pygame.MOUSEBUTTONDOWN and self.continueGame:
                if self.debounce == False:
                    self.debounce = True
                    self.draggingPiece = True

                    imageTile = self.checkImageTilePressed(mousePos)
                    self.prevImageTile = imageTile

                    #TODO: this is temporary, make it better
                    moves = self.gameBoard.generateMoves()
                    for move in moves:
                        if move.getStartSquare() == imageTile.getTileNumber():
                        
                            for row in self.imageBoard:
                                for imageTileToHighlight in row:
                                    if move.getTargetSquare() == imageTileToHighlight.getTileNumber():
                                        imageTileToHighlight.highlight()

                    self.imagePieceDragged = imageTile.getImagePiece()

            elif event.type == pygame.MOUSEBUTTONUP and self.continueGame:
                self.debounce = False
                self.draggingPiece = False
                
                if self.imagePieceDragged != None:
                    imageTile = self.checkImageTilePressed(mousePos)

                    #TODO: make this shit better
                    moves = self.gameBoard.generateMoves()
                    for move in moves:
                        if move.getStartSquare() == self.prevImageTile.getTileNumber():
                            for row in self.imageBoard:
                                for imageTileToHighlight in row:
                                    if move.getTargetSquare() == imageTileToHighlight.getTileNumber():
                                        imageTileToHighlight.removeHighlight()
                    
                    # this could be better by making moves a dict and have constant lookups instead of linear
                    for move in moves:
                        if move.getStartSquare() == self.prevImageTile.getTileNumber() and move.getTargetSquare() == imageTile.getTileNumber():
                            self.gameBoard.move(move)
                            if self.colorToMove == 'w':
                                self.colorToMove = 'b'
                            else:
                                self.colorToMove = 'w'

                            break

                    prevMove = PrevMove("tempColorToMove", self.prevImageTile, imageTile, self.prevImageTile.getImagePiece(), imageTile.getImagePiece())
                    self.moveHistory.append(prevMove)

                    self.prevImageTile.setImagePiece(None)

                    imageTile.setImagePiece(self.imagePieceDragged, self.imagePieceGroup)

                    self.imagePieceDragged.placeDown(imageTile.getCoords())

                self.imagePieceDragged = None
                self.prevImageTile = None

            elif event.type == pygame.MOUSEMOTION and self.draggingPiece:
                if self.imagePieceDragged != None:
                    self.imagePieceDragged.setDrawTo(mousePos)
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                self.undoMove()

    
    def checkImageTilePressed(self, mousePos):
        for row in self.imageBoard:
            for imageTile in row:
                if imageTile.pressed(mousePos):
                    return imageTile
    
    def undoMove(self):
        if len(self.moveHistory) > 0:
            self.gameBoard.undoMove()

            moveToUndo = self.moveHistory.pop()
            startSquare = moveToUndo.startSquare
            targetSquare = moveToUndo.targetSquare
            startSquarePiece = moveToUndo.startSquarePiece
            targetSquarePiece = moveToUndo.targetSquarePiece

            startSquare.setImagePiece(startSquarePiece, self.imagePieceGroup)
            targetSquare.setImagePiece(targetSquarePiece, self.imagePieceGroup)


class ImageTile(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color, surface, tileNumber):
        super().__init__()
        self.x = x
        self.y = y
        self.surface = surface
        self.tileNumber = tileNumber
        self.origColor = color
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.isClicked = False
        self.imagePiece = None
        self.captureSound = pygame.mixer.Sound("./sounds/public_sound_standard_Capture.wav")
    
    def highlight(self):
        if self.origColor == "#769656":
            self.image.fill(pygame.Color("#cc0000"))
        else:
            self.image.fill(pygame.Color("#ff4d4d"))
    
    def removeHighlight(self):
        self.image.fill(pygame.Color(self.origColor))
    
    def setInitImagePiece(self, imagePiece):
        self.imagePiece = imagePiece
    
    def setImagePiece(self, imagePiece, imagePieceGroup=None):
        if imagePieceGroup != None and self.imagePiece in imagePieceGroup:
            self.captureSound.play()
            imagePieceGroup.remove(self.imagePiece)
        elif imagePieceGroup != None and imagePiece != None and imagePiece not in imagePieceGroup:
            imagePieceGroup.add(imagePiece)
        self.imagePiece = imagePiece

    def getImagePiece(self):
        return self.imagePiece

    def pressed(self, mousePos):
        return pygame.Rect.collidepoint(self.rect, mousePos)
    
    def getCoords(self):
        return (self.x, self.y)
    
    def getTileNumber(self):
        return self.tileNumber

class ImagePiece(pygame.sprite.Sprite):
    def __init__(self, image, imageTile, surface):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.drawTo = imageTile.getCoords()
        self.rect.topleft = self.drawTo
        self.surface = surface
        self.moveSound = pygame.mixer.Sound("./sounds/public_sound_standard_Move.wav")
        
    
    def getImage(self):
        return self.image
    
    def placeDown(self, newDrawTo):
        self.moveSound.play()
        self.rect.topleft = newDrawTo
        
    
    def setDrawTo(self, newDrawTo):
        self.rect.center = newDrawTo


class FenString:
    def __init__(self):
            self.fenString = None
            self.colorToMove = None
            self.askForFenString()
    
    def getString(self):
        return self.fenString
    
    def askForFenString(self):
        userInput = input("Y for starting FEN, otherwise input FEN: ")
        
        if userInput.lower() == "y":
            fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
            self.fenString, self.colorToMove = fenString.split(" ")

        else:
            self.fenString, self.colorToMove = userInput.split(" ")
    
    def getColorToMove(self):
        return self.colorToMove

    def generateCurrentFen(self):
        pass



class PrevMove:
    def __init__(self, colorToMove, startSquare, targetSquare, startSquarePiece, targetSquarePiece):
        self.colorToMove = colorToMove
        self.startSquare = startSquare
        self.targetSquare = targetSquare
        self.startSquarePiece = startSquarePiece
        self.targetSquarePiece = targetSquarePiece

main()