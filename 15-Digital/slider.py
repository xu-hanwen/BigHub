import pygame, sys, random
from pygame.locals import *  # 导入常量变量

# 游戏参数配置
BOARDWIDTH = 4  # 游戏板列数
BOARDHEIGHT = 4 # 游戏板行数
TILESIZE = 80   # 游戏块大小
WINDOWWIDTH = 640  # 窗口大小
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

# 配置颜色
#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)   # 文本颜色
BRIGHTBLUE =    (  0,  50, 255)   # 滑块颜色
DARKTURQUOISE = (  3,  54,  73)   # 背景颜色
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE   
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20   # 字体大小

BUTTONCOLOR = WHITE               
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
# 窗口边距
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# 配置动作
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    # 游戏循环的每次迭代都设置一个暂停
    FPSCLOCK = pygame.time.Clock()
    # 窗口
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    # 创建字体对象（字体类型和大小）
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # 界面的可点击按钮
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    # 返回当前状态和随机移动序列（80代表随机移动次数）
    mainBoard, solutionSeq = generateNewPuzzle(40)
    print(mainBoard,solutionSeq)
    # 获取目标状态
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
    # 求解移动序列
    allMoves = [] # list of moves made from the solved configuration

    # 游戏主循环
    while True: # main game loop
        slideTo = None # 记录玩家移动方向
        msg = 'Click tile or press arrow keys to slide.' # 窗口顶部显示的字符
        if mainBoard == SOLVEDBOARD:   # 当前状态和目标状态相同
            msg = 'Solved!'

        drawBoard(mainBoard, msg)  # 绘制当前状态

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                        allMoves = []
                else:
                    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)


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


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # 绘制滑块
    # adjx：滑块动画x位移像素
    # adjy: 滑块动画y位移像素
    # number: 方块显示信息
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)

    picture_src = "image/image" + str(number) + ".jpeg"
    image = pygame.image.load(picture_src)
    image_rect = image.get_rect()
    image_rect.topleft = (left + adjx, top + adjy)
    DISPLAYSURF.blit(image, image_rect)

    # pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    # textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    # textRect = textSurf.get_rect()
    # textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    # DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # 点击按钮
    textSurf = BASICFONT.render(text, True, color, bgcolor)  # 文本绘制到背景上面
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)     # 设置文本所在位置
    return (textSurf, textRect)


def drawBoard(board, message):
    # message:左上角提示信息
    DISPLAYSURF.fill(BGCOLOR)
    if message:  # 显示提示信息
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    # 绘制滑块
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    # 绘制边框
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
    # 绘制按钮
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.
    # 根据空白滑块索引获取移动滑块索引
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)  # 绘制画板
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    # 绘制滑动效果
    for i in range(0, TILESIZE, animationSpeed):
        # animatespeed：步长偏移速度
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    """重新开始游戏"""
    # numslides：移动次数
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()  # 目标状态
    drawBoard(board, '')   # 绘制画板
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove) # 随机移动方向
        # 绘制滑块效果
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)  # 改变游戏状态
        sequence.append(move)  # 记录移动信息
        lastMove = move
    return (board, sequence)  # 返回当前游戏状态和历史移动信息


def resetAnimation(board, allMoves):
    """重置步骤"""
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()   # 翻转操作列表

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        # 移动效果
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)  # 更新状态


if __name__ == '__main__':
    main()