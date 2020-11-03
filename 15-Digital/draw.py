import pygame,sys,threading
import game_function as gf
from settings import *


class Draw():
    """包含所有的绘画操作类"""
    def __init__(self,screen,FONT,FPS_CLOCK):
        self.screen = screen
        self.FONT = FONT
        self.FPS_CLOCK = FPS_CLOCK

    def draw_tile(self,tilex, tiley, number, adjx=0, adjy=0):
        # 绘制滑块
        # adjx：滑块动画x位移像素
        # adjy: 滑块动画y位移像素
        # number: 方块显示信息
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = gf.getLeftTopOfTile(tilex, tiley)

        picture_src = "image/image" + str(number) + ".jpeg"
        image = pygame.image.load(picture_src)
        image_rect = image.get_rect()
        image_rect.topleft = (left + adjx, top + adjy)
        self.screen.blit(image, image_rect)

    def draw_tile_r(self,tilex, tiley, number, adjx=0, adjy=0):
        # 绘制滑块
        # adjx：滑块动画x位移像素
        # adjy: 滑块动画y位移像素
        # number: 方块显示信息
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = gf.getLeftTopOfTile_r(tilex, tiley)

        picture_src = "image/image" + str(number) + ".jpeg"
        image = pygame.image.load(picture_src)
        image_rect = image.get_rect()
        image_rect.topleft = (left + adjx, top + adjy)
        self.screen.blit(image, image_rect)

    def makeText(self,text, color, bgcolor, top, left):
        # 点击按钮
        textSurf = self.FONT.render(text, True, color, bgcolor)  # 文本绘制到背景上面
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)     # 设置文本所在位置
        return (textSurf, textRect)


    def drawBoard(self,board,board_r, message):
        # message:左上角提示信息
        self.screen.fill(BGCOLOR)
        if message:  # 显示提示信息
            textSurf, textRect = self.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
            self.screen.blit(textSurf, textRect)

        # 绘制滑块
        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:
                    self.draw_tile(tilex, tiley, board[tilex][tiley])
                if board_r[tilex][tiley]:
                    self.draw_tile_r(tilex,tiley,board_r[tilex][tiley])

        # 绘制边框
        left, top = gf.getLeftTopOfTile(0, 0)
        left_r, top_r = gf.getLeftTopOfTile_r(0, 0)
        width = BOARDWIDTH * TILESIZE
        height = BOARDHEIGHT * TILESIZE
        pygame.draw.rect(self.screen, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
        pygame.draw.rect(self.screen, BORDERCOLOR, (left_r - 5, top_r - 5, width + 11, height + 11), 4)
        # 绘制按钮
        RESET_SURF, RESET_RECT = self.makeText('重置', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 150)
        NEW_SURF, NEW_RECT = self.makeText('再来一局', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
        SOLVE_SURF, SOLVE_RECT = self.makeText('人机对战', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
        BATTLE_SURF, BATTLE_RECT = self.makeText('算法对比', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)

        self.screen.blit(RESET_SURF, RESET_RECT)
        self.screen.blit(NEW_SURF, NEW_RECT)
        self.screen.blit(SOLVE_SURF, SOLVE_RECT)
        self.screen.blit(BATTLE_SURF,BATTLE_RECT)


    def slideAnimation(self,board,board_r,direction,direction_r, message, animationSpeed,msg_l='',msg_r='',time_spent_a='',time_spent_b=''):
        # Note: This function does not check if the move is valid.
        # 根据空白滑块索引获取移动滑块索引
        blankx, blanky = gf.getBlankPosition(board)
        blankx_r, blanky_r = gf.getBlankPosition(board_r)
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

        if direction_r == UP:
            movex_r = blankx_r
            movey_r = blanky_r + 1
        elif direction_r == DOWN:
            movex_r = blankx_r
            movey_r = blanky_r - 1
        elif direction_r == LEFT:
            movex_r = blankx_r + 1
            movey_r = blanky_r
        elif direction_r == RIGHT:
            movex_r = blankx_r - 1
            movey_r = blanky_r

        # prepare the base surface
        self.drawBoard(board,board_r, message)  # 绘制画板
        msg_l_surf, msg_l_rect = self.makeText(msg_l, MESSAGECOLOR, BGCOLOR, 295, 45)
        time_l_surf, time_l_rect = self.makeText(time_spent_a, MESSAGECOLOR, BGCOLOR, 275, 15)
        msg_r_surf, msg_r_rect = self.makeText(msg_r, MESSAGECOLOR, BGCOLOR, 940, 45)
        time_r_surf, time_r_rect = self.makeText(time_spent_b, MESSAGECOLOR, BGCOLOR, 915, 15)
        self.screen.blit(msg_r_surf, msg_r_rect)
        self.screen.blit(msg_l_surf, msg_l_rect)  # 显示消息
        self.screen.blit(time_l_surf,time_l_rect)
        self.screen.blit(time_r_surf,time_r_rect)
        baseSurf = self.screen.copy()
        # draw a blank space over the moving tile on the baseSurf Surface.
        if direction != None:
            moveLeft, moveTop = gf.getLeftTopOfTile(movex, movey)
            pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

        if direction_r != None:
            moveLeft_r, moveTop_r = gf.getLeftTopOfTile_r(movex_r, movey_r)
            pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft_r, moveTop_r, TILESIZE, TILESIZE))

        # 绘制滑动效果
        for i in range(0, TILESIZE, animationSpeed):
            # animatespeed：步长偏移速度
            gf.checkForQuit()
            self.screen.blit(baseSurf, (0, 0))
            if direction != None:
                if direction == UP:
                    self.draw_tile(movex, movey, board[movex][movey], 0, -i)
                if direction == DOWN:
                    self.draw_tile(movex, movey, board[movex][movey], 0, i)
                if direction == LEFT:
                    self.draw_tile(movex, movey, board[movex][movey], -i, 0)
                if direction == RIGHT:
                    self.draw_tile(movex, movey, board[movex][movey], i, 0)

            if direction_r != None:
                if direction_r == UP:
                    self.draw_tile_r(movex_r, movey_r, board_r[movex_r][movey_r], 0, -i)
                if direction_r == DOWN:
                    self.draw_tile_r(movex_r, movey_r, board_r[movex_r][movey_r], 0, i)
                if direction_r == LEFT:
                    self.draw_tile_r(movex_r, movey_r, board_r[movex_r][movey_r], -i, 0)
                if direction_r == RIGHT:
                    self.draw_tile_r(movex_r, movey_r, board_r[movex_r][movey_r], i, 0)

            pygame.display.update()
            self.FPS_CLOCK.tick(FPS)

    def generateNewPuzzle(self,numSlides):
        """重新开始游戏"""
        sequence = []
        board = gf.getStartingBoard()  # 目标状态
        board_r = gf.getStartingBoard()
        self.drawBoard(board, board_r,'')   # 绘制画板
        pygame.display.update()
        pygame.time.wait(1000) # pause 500 milliseconds for effect
        lastMove = None
        for i in range(numSlides):
            move = gf.getRandomMove(board, lastMove) # 随机移动方向
            move_r = move
            # 绘制滑块效果
            self.slideAnimation(board,board_r, move,move_r, '正在准备游戏', animationSpeed=animationSpeed+10)
            gf.makeMove(board, move)  # 改变游戏状态
            gf.makeMove(board_r,move_r)
            sequence.append(move)  # 记录移动信息
            lastMove = move
        return (board,board_r, sequence)  # 返回当前游戏状态和历史移动信息


    def resetAnimation(self,board,board_r, allMoves,message=''):
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
            self.slideAnimation(board,board_r,None,oppositeMove, message, animationSpeed=animationSpeed)
            pygame.time.wait(0)
            gf.makeMove(board_r, oppositeMove)  # 更新状态

    def resetAnimation_l(self,board,board_r, allMoves):
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
            self.slideAnimation(board,board_r,oppositeMove,None, '', animationSpeed=animationSpeed)
            pygame.time.wait(0)
            gf.makeMove(board, oppositeMove)  # 更新状态

    def thread_move(self,revAllMoves_l, revAllMoves_r, mainBoard, mainBoard_r, message, msg_l, msg_r,time_spent_a='',time_spent_b=''):
        # 多线程
        threadLock = threading.Lock()
        threads = []

        while (len(revAllMoves_r)>0)&(len(revAllMoves_l)>0):
            move_l = revAllMoves_l.pop()
            if move_l == UP:
                oppositeMove_l = DOWN
            elif move_l == DOWN:
                oppositeMove_l = UP
            elif move_l == RIGHT:
                oppositeMove_l = LEFT
            elif move_l == LEFT:
                oppositeMove_l = RIGHT

            move_r = revAllMoves_r.pop()
            if move_r == UP:
                oppositeMove_r = DOWN
            elif move_r == DOWN:
                oppositeMove_r = UP
            elif move_r == RIGHT:
                oppositeMove_r = LEFT
            elif move_r == LEFT:
                oppositeMove_r = RIGHT

            # 移动效果
            def run(mainBoard, mainBoard_r, oppositeMove_l, oppositeMove_r, message, msg_l, msg_r,time_spent_a,time_spent_b, msg='A'):
                if msg == 'A':
                    threadLock.acquire()
                    self.slideAnimation(mainBoard, mainBoard_r, oppositeMove_l, None, message, animationSpeed-2, msg_l,
                                          msg_r,time_spent_a,time_spent_b)
                    gf.makeMove(mainBoard, oppositeMove_l)  # 更新状态
                    threadLock.release()
                else:
                    threadLock.acquire()
                    self.slideAnimation(mainBoard, mainBoard_r, None, oppositeMove_r, message, animationSpeed-4, msg_l,
                                          msg_r,time_spent_a,time_spent_b)
                    gf.makeMove(mainBoard_r, oppositeMove_r)  # 更新状态
                    threadLock.release()

            t2 = threading.Thread(target=run, args=(
                mainBoard, mainBoard_r, oppositeMove_l, oppositeMove_r, message, msg_l, msg_r,time_spent_a,time_spent_b))
            t1 = threading.Thread(target=run,
                                  args=(
                                  mainBoard, mainBoard_r, oppositeMove_l, oppositeMove_r, message, msg_l, msg_r,time_spent_a,time_spent_b,' '))
            t1.start()
            t2.start()
            threads.append(t1)
            threads.append(t2)

            for t in threads:
                t.join()
