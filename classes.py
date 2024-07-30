import pygame
import math

class square():
    def __init__(self,number,letter,color,rect,pos,width,height,piece=None):
        self.letter = letter
        self.number = number
        self.color = color
        self.rect = rect
        self.pos = pos
        self.width = width
        self.height = height
        self.occupied = False
        self.piece = piece
        self.selected = False

    def setLetter(self,letter):
        self.letter = letter
    
    def setNumber(self,number):
        self.number = number

    def setColor(self,color):
        self.color = color

    def setRect(self,rect):
        self.rect = rect
    
    def setOccupied(self,occupied):
        self.occupied = occupied

    def setPiece(self,piece):
        self.piece = piece

class piece():
    def __init__(self,type,color,image,pos):
        self.type = type
        self.color = color
        temp = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(temp,(65,65))
        self.captured = False
        self.pos = pos
        self.moves = 0
        self.possibleMoves = []
        self.availableMoves = []
        self.setPossibleMoves()

    def setPossibleMoves(self):
        if self.type == "pawn":
            if self.color == "white":
                direction = 1
            elif self.color == "black":
                direction = -1
            if self.moves == 0:
                self.possibleMoves = [(2*direction,0),(direction,0)]
            else:
                self.possibleMoves = [(direction,0)]
        if self.type == "rook":
            for i in range(8-self.pos[0]):
                self.possibleMoves.append((i+1,0))
            for j in range(8-self.pos[1]):
                self.possibleMoves.append((0,j+1))
            for i in range(self.pos[0]-1):
                self.possibleMoves.append((i-7,0))
            for j in range(self.pos[1]):
                self.possibleMoves.append((0,-j))
        if self.type == "knight":
            for i in [-1,1]:
                for j in [-2,2]:
                    self.possibleMoves.append((i,j))
            for i in [-2,2]:
                for j in [-1,1]:
                    self.possibleMoves.append((i,j))
        if self.type == "bishop":
            for i in range(8-self.pos[0]):
                self.possibleMoves.append((i+1,i+1))
                self.possibleMoves.append((i+1,-(i+1)))
            for i in range(self.pos[0]-1):
                self.possibleMoves.append((i-7,i-7))
                self.possibleMoves.append((i-7,-(i-7)))
        if self.type == "queen":
            for i in range(8-self.pos[0]):
                self.possibleMoves.append((i+1,i+1))
                self.possibleMoves.append((i+1,-(i+1)))
                self.possibleMoves.append((i+1,0))
            for i in range(self.pos[0]-1):
                self.possibleMoves.append((i-7,i-7))
                self.possibleMoves.append((i-7,-(i-7)))
                self.possibleMoves.append((i-7,0))
            for j in range(8-self.pos[1]):
                self.possibleMoves.append((0,j+1))
            for j in range(self.pos[1]):
                self.possibleMoves.append((0,-j))
        if self.type == "king":
            self.possibleMoves = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
            

    def setPos(self,pos):
        self.pos = pos

    def setCaptured(self,captured):
        self.captured = captured

    def setMoves(self,moves):
        self.moves = moves