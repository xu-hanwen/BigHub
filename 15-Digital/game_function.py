import pygame,random,sys
from settings import *
from pygame.locals import *  # 导入常量变量

def terminate():
        # 程序退出函数
        pygame.quit()
        sys.exit()

def checkForQuit():
    """检查强制退出"""
    # quit和espace
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # put the other KEYUP event objects back

def getStartingBoard():
    # 返回目标状态
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    # 返回空白格子索引
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # 移动方块
    blankx, blanky = getBlankPosition(board)  # 返回空白格子索引
    # 方块移动不是空格
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    # 方块不合法移动判断
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
            (move == DOWN and blanky != 0) or \
            (move == LEFT and blankx != len(board) - 1) or \
            (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    """返回一个随机移动方向"""
    # lastMove:上次移动记录
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # 排除上下重复移动和上下不合法移动
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    # 排除左右重复移动和左右不合法移动
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    """根据索引返回像素坐标"""
    # tileX-1:格子间距
    left = XMARGIN+4 + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN+4 + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def getLeftTopOfTile_r(tileX, tileY):
    """根据索引返回像素坐标"""
    # tileX-1:格子间距
    left = XMARGIN_r+4 + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN+4 + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # 根据像素坐标找到数据索引
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):  # 判断像素坐标是否在矩形内
                return (tileX, tileY)   # 返回索引
    return (None, None)

def getSpotClicked_r(board, x, y):
    # 根据像素坐标找到数据索引
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left_r, top_r = getLeftTopOfTile_r(tileX, tileY)
            tileRect_r = pygame.Rect(left_r, top_r, TILESIZE, TILESIZE)
            if tileRect_r.collidepoint(x, y):  # 判断像素坐标是否在矩形内
                return (tileX, tileY)   # 返回索引
    return (None, None)



