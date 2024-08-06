from classes import *

def get_font(size):
	return pygame.font.Font("assets\\LucidaBrightRegular.ttf",size)

def drawBoard():
    pygame.draw.rect(board,(255,255,255),pygame.Rect(98,48,604,604))
    color = 1
    letters = ['a','b','c','d','e','f','g','h']
    #numbers
    # i is row
    # j is column
    occupy = []
    occupy.append(whitePieces[0])
    occupy.append(whitePieces[1])
    for ii in range(4):
        occupy.append([])
        for jj in range(8):
            occupy[ii+2].append(None)
    occupy.append(blackPieces[0])
    occupy.append(blackPieces[1])

    for i in range(8):
        for j in range(8):
            if j % 2 == 0:
                if color % 2 == 1:
                    rect = pygame.draw.rect(board,(144,144,144),pygame.Rect(100+(SCREEN_WIDTH/8*j),50+(SCREEN_HEIGHT/8*(7-i)),SCREEN_WIDTH/8,SCREEN_HEIGHT/8))
                else:
                    rect = pygame.draw.rect(board,(255,255,255),pygame.Rect(100+(SCREEN_WIDTH/8*j),50+(SCREEN_HEIGHT/8*(7-i)),SCREEN_WIDTH/8,SCREEN_HEIGHT/8))
            else:
                if color % 2 == 1:
                    rect = pygame.draw.rect(board,(255,255,255),pygame.Rect(100+(SCREEN_WIDTH/8*j),50+(SCREEN_HEIGHT/8*(7-i)),SCREEN_WIDTH/8,SCREEN_HEIGHT/8))
                else:
                    rect = pygame.draw.rect(board,(144,144,144),pygame.Rect(100+(SCREEN_WIDTH/8*j),50+(SCREEN_HEIGHT/8*(7-i)),SCREEN_WIDTH/8,SCREEN_HEIGHT/8))
            if color % 2 == 1:
                sq = square(i+1,j+1,"black",rect,(100+(SCREEN_WIDTH/8*j),50+(SCREEN_HEIGHT/8*(7-i))),SCREEN_WIDTH/8,SCREEN_HEIGHT/8,occupy[i][j])
            else:
                sq = square(i+1,j+1,"white",rect,(100+(SCREEN_WIDTH/8*j),50+(SCREEN_HEIGHT/8*(7-i))),SCREEN_WIDTH/8,SCREEN_HEIGHT/8,occupy[i][j])
            squares[i].append(sq)
        color += 1
        board.blit(get_font(20).render(str(i+1),True,"#ffffff"),(80,(squares[i][0].pos[1]+squares[0][0].height/2)-12))
        board.blit(get_font(20).render(str(i+1),True,"#ffffff"),(710,(squares[i][0].pos[1]+squares[0][0].height/2)-12))
        board.blit(get_font(20).render(letters[i],True,"#ffffff"),((squares[0][i].pos[0]+squares[0][0].width/2)-5,20))
        board.blit(get_font(20).render(letters[i],True,"#ffffff"),((squares[0][i].pos[0]+squares[0][0].width/2)-5,650))

def drawPieces():
    occupy = []
    occupy.append(whitePieces[0])
    occupy.append(whitePieces[1])
    for ii in range(4):
        occupy.append([])
        for jj in range(8):
            occupy[ii+2].append(None)
    occupy.append(blackPieces[0])
    occupy.append(blackPieces[1])
    for i in range(2):
        for j in range(8):
            if occupy[i][j] != None:
                squares[i][j].setOccupied(True)
                pieces_surf.blit(occupy[i][j].image,(squares[i][j].pos[0]+4,squares[i][j].pos[1]))
    
    for i in range(2):
        for j in range(8):
            if occupy[i+6][j] != None:
                squares[i+6][j].setOccupied(True)
                pieces_surf.blit(occupy[i+6][j].image,(squares[i+6][j].pos[0]+4,squares[i+6][j].pos[1]))

def drawPossibleMoves(piece):
    if piece.type == "pawn":
        piece.setPossibleMoves()
        if piece.color == "white":
            if 0 <= piece.pos[1] < len(squares[piece.pos[0]]) and squares[piece.pos[0]][piece.pos[1]].occupied == True:
                piece.possibleMoves.append((1,1))
            if 0 <= piece.pos[1]-2 < len(squares[piece.pos[0]]) and squares[piece.pos[0]][piece.pos[1]-2].occupied == True:
                piece.possibleMoves.append((1,-1))
        elif piece.color == "black":
            if 0 <= piece.pos[1] < len(squares[piece.pos[0]-2]) and squares[piece.pos[0]-2][piece.pos[1]].occupied == True:
                piece.possibleMoves.append((-1,1))
            if 0 <= piece.pos[1]-2 < len(squares[piece.pos[0]-2]) and squares[piece.pos[0]-2][piece.pos[1]-2].occupied == True:
                piece.possibleMoves.append((-1,-1))
    pos = piece.pos
    possible = []
    for i in piece.possibleMoves:
        if piece.pos[0]+i[0] <= 8 and piece.pos[1]+i[1] <= 8 and piece.pos[0]+i[0] >= 1 and piece.pos[1]+i[1] >=1:
            # if squares[piece.pos[0]+i[0]-1][piece.pos[1]+i[1]-1].occupied == False:
            if squares[piece.pos[0]+i[0]-1][piece.pos[1]+i[1]-1].piece == None or squares[piece.pos[0]+i[0]-1][piece.pos[1]+i[1]-1].piece.color != piece.color:
                possible.append((piece.pos[0]+i[0],piece.pos[1]+i[1]))
    piece.availableMoves = possible
    for i in possible:
        center = (squares[i[0]-1][i[1]-1].pos[0] + squares[0][0].width/2, squares[i[0]-1][i[1]-1].pos[1] + squares[0][0].height/2)
        pygame.draw.circle(playing_surf,(255,255,0,90),center,20)

def movePiece(piece,newPos):
    squares[piece.pos[0]-1][piece.pos[1]-1].setOccupied(False)
    if squares[newPos[0]-1][newPos[1]-1].piece and squares[newPos[0]-1][newPos[1]-1].piece.color != piece.color:
        squares[newPos[0]-1][newPos[1]-1].piece.setCaptured(True)
        captured_pieces.append(squares[newPos[0]-1][newPos[1]-1])
    squares[newPos[0]-1][newPos[1]-1].piece = squares[piece.pos[0]-1][piece.pos[1]-1].piece
    if squares[piece.pos[0]-1][piece.pos[1]-1] != squares[newPos[0]-1][newPos[1]-1]:
        squares[piece.pos[0]-1][piece.pos[1]-1].piece = None
    squares[newPos[0]-1][newPos[1]-1].setOccupied(True)
    pieces_surf.fill(pygame.Color(0,0,0,0))
    piece.pos = newPos
    piece.moves += 1
    for i in [whitePieces[0],whitePieces[1],blackPieces[0],blackPieces[1]]:
        for j in range(8):
            if i[j].captured == False:
                pieces_surf.blit(i[j].image,(squares[i[j].pos[0]-1][i[j].pos[1]-1].pos[0]+4,squares[i[j].pos[0]-1][i[j].pos[1]-1].pos[1]))

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH+200, SCREEN_HEIGHT+100))
pygame.display.set_caption("PyChess")
pygame.display.set_icon(pygame.image.load("assets\\icon1.png"))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000
board = pygame.Surface((SCREEN_WIDTH+200,SCREEN_HEIGHT+100),pygame.SRCALPHA,32)
board.convert_alpha()
pieces_surf = pygame.Surface((SCREEN_WIDTH+200,SCREEN_HEIGHT+100),pygame.SRCALPHA,32)
pieces_surf.convert_alpha()
playing_surf = pygame.Surface((SCREEN_WIDTH+200,SCREEN_HEIGHT+100),pygame.SRCALPHA,32)
playing_surf.convert_alpha()
squares = []
blackPieces = [[],[piece("rook","black","assets\\black-rook.png",(8,1)),piece("knight","black","assets\\black-knight.png",(8,2)),piece("bishop","black","assets\\black-bishop.png",(8,3)),piece("queen","black","assets\\black-queen.png",(8,4)),
piece("king","black","assets\\black-king.png",(8,5)),piece("bishop","black","assets\\black-bishop.png",(8,6)),piece("knight","black","assets\\black-knight.png",(8,7)),piece("rook","black","assets\\black-rook.png",(8,8))]]
for i in range(8):
    blackPieces[0].append(piece("pawn","black","assets\\black-pawn.png",(7,i+1)))
whitePieces = [[piece("rook","white","assets\\white-rook.png",(1,1)),piece("knight","white","assets\\white-knight.png",(1,2)),piece("bishop","white","assets\\white-bishop.png",(1,3)),piece("queen","white","assets\\white-queen.png",(1,4)),
piece("king","white","assets\\white-king.png",(1,5)),piece("bishop","white","assets\\white-bishop.png",(1,6)),piece("knight","white","assets\\white-knight.png",(1,7)),piece("rook","white","assets\\white-rook.png",(1,8))],[]]
for i in range(8):
    whitePieces[1].append(piece("pawn","white","assets\\white-pawn.png",(2,i+1)))
captured_pieces = []
for i in range (8):
    squares.append([])
drawBoard()
drawPieces()

running = True
selected = None
selected_piece = None
selected_pos = (0,0)
global turn
turn = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if selected_piece == None:
                if mouse[0] < 100 or mouse[1] < 50 or mouse[0] > 700 or mouse[1] > 650:
                    selected = None
                    selected_pos = None
                    selected_piece = None
                else:
                    x = mouse[0] - 100
                    y = 650 - mouse[1]
                    column = math.ceil(x/squares[0][0].width)
                    row = math.ceil(y/squares[0][0].height)
                    playing_surf.fill(pygame.Color(0,0,0,0))
                    if squares[row-1][column-1].occupied == True:
                        if turn % 2 == 1:
                            if squares[row-1][column-1].piece.color == "white":
                                selected_pos = (squares[row-1][column-1].pos[0],squares[row-1][column-1].pos[1])
                                selected_piece = squares[row-1][column-1].piece
                                selected = pygame.draw.rect(playing_surf,(255,255,0,50),pygame.Rect(selected_pos[0],selected_pos[1],squares[0][0].width,squares[0][0].height))
                                drawPossibleMoves(squares[row-1][column-1].piece)
                        else:
                            if squares[row-1][column-1].piece.color == "black":
                                selected_pos = (squares[row-1][column-1].pos[0],squares[row-1][column-1].pos[1])
                                selected_piece = squares[row-1][column-1].piece
                                selected = pygame.draw.rect(playing_surf,(255,255,0,50),pygame.Rect(selected_pos[0],selected_pos[1],squares[0][0].width,squares[0][0].height))
                                drawPossibleMoves(squares[row-1][column-1].piece)
            else:
                if mouse[0] < 100 or mouse[1] < 50 or mouse[0] > 700 or mouse[1] > 650:
                    selected = None
                    selected_pos = None
                    selected_piece = None
                else:
                    x = mouse[0] - 100
                    y = 650 - mouse[1]
                    column = math.ceil(x/squares[0][0].width)
                    row = math.ceil(y/squares[0][0].height)
                    if (row,column) in selected_piece.availableMoves:
                        movePiece(selected_piece,(row,column))
                        turn += 1
                    selected = selected_piece = selected_pos = None

    screen.fill("black")
    screen.blit(board,(0,0))
    if selected != None:
        screen.blit(playing_surf,(0,0))
    screen.blit(pieces_surf,(0,0))
    pygame.display.flip()