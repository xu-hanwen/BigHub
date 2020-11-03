from draw import Draw
from settings import *
from picture import image
import game_function as gf
from pygame.locals import *  # 导入常量变量
from a import getPath as getPath_a
from astar import getPath as getPath_astar
from shendu import getPath as getPath_shendu
import pygame,sys,os,copy,threading,datetime


def run_main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    pygame.init()
    # 游戏循环的每次迭代都设置一个暂停
    FPSCLOCK = pygame.time.Clock()
    # 窗口
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('数码难')
    # 创建字体对象（字体类型和大小）
    BASICFONT = pygame.font.Font('C:\Windows\Fonts\simsun.ttc', BASICFONTSIZE)

    slider = Draw(DISPLAYSURF,BASICFONT,FPSCLOCK)
    # 界面的可点击按钮
    RESET_SURF, RESET_RECT = slider.makeText('重置',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 150)
    NEW_SURF,   NEW_RECT   = slider.makeText('再来一局', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
    SOLVE_SURF, SOLVE_RECT = slider.makeText('人机对战',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    BATTLE_SURF,BATTLE_RECT = slider.makeText('算法对比',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)

    # 返回当前状态和随机移动序列（80代表随机移动次数）
    mainBoard,mainBoard_r, solutionSeq = slider.generateNewPuzzle(20)

    # 获取目标状态
    SOLVEDBOARD = gf.getStartingBoard()
    # 求解移动序列
    allMoves = []
    allMoves_r = []
    message_result_l,message_result_r = None,None


    # 游戏主循环
    while True:
        slideTo = None  # 记录玩家移动方向
        slideTo_r = None
        msg = '点击按键滑动窗口' # 窗口顶部显示的字符
        if mainBoard == SOLVEDBOARD :   # 当前状态和目标状态相同
            msg = message_result_l
        elif mainBoard_r == SOLVEDBOARD:
            msg = message_result_r
        slider.drawBoard(mainBoard,mainBoard_r, msg)  # 绘制当前状态

        gf.checkForQuit()   # 检测退出
        # 键鼠移动检测
        for event in pygame.event.get():
            # 右侧键盘控制部分
            if event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and gf.isValidMove(mainBoard_r, LEFT):
                    slideTo_r = LEFT
                elif event.key in (K_RIGHT, K_d) and gf.isValidMove(mainBoard_r, RIGHT):
                    slideTo_r = RIGHT
                elif event.key in (K_UP, K_w) and gf.isValidMove(mainBoard_r, UP):
                    slideTo_r = UP
                elif event.key in (K_DOWN, K_s) and gf.isValidMove(mainBoard_r, DOWN):
                    slideTo_r = DOWN
            if event.type == MOUSEBUTTONUP:
                # 左侧鼠标控制部分
                spotx, spoty = gf.getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) != (None, None):
                    blankx, blanky = gf.getBlankPosition(mainBoard)
                    # 左边
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

                # 右侧鼠标控制部分
                spotx_r, spoty_r = gf.getSpotClicked_r(mainBoard_r, event.pos[0], event.pos[1])
                if (spotx_r, spoty_r) != (None, None):
                    # 右边
                    blankx_r, blanky_r = gf.getBlankPosition(mainBoard_r)
                    if spotx_r == blankx_r + 1 and spoty_r == blanky_r:
                        slideTo_r = LEFT
                    elif spotx_r == blankx_r - 1 and spoty_r == blanky_r:
                        slideTo_r = RIGHT
                    elif spotx_r == blankx_r and spoty_r == blanky_r + 1:
                        slideTo_r = UP
                    elif spotx_r == blankx_r and spoty_r == blanky_r - 1:
                        slideTo_r = DOWN
                else:
                    if RESET_RECT.collidepoint(event.pos):
                        # 更新左上角状态信息
                        message = "正在重置到初始状态"
                        textSurf, textRect = slider.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
                        slider.screen.blit(textSurf, textRect)
                        # 更新状态并绘图
                        slider.resetAnimation(mainBoard,mainBoard_r, allMoves_r)
                        allMoves_r = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard,mainBoard_r, solutionSeq = slider.generateNewPuzzle(20)
                        allMoves_r,allMoves = [],[]
                    elif BATTLE_RECT.collidepoint(event.pos):
                        message = "算法对比ing"
                        textSurf, textRect = slider.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
                        slider.screen.blit(textSurf, textRect)

                        msg_l = "A算法"
                        msg_r = "A*算法"
                        message_result_l, message_result_r = msg_l+'胜利！',msg_r+'胜利！'

                        board_input_A = copy.deepcopy(mainBoard)  # 由于算法限制，此处做一个深拷贝
                        start_A = datetime.datetime.now()
                        # @TODO 算法A接口
                        solution_l = getPath_a(board_input_A)
                        revAllMoves_l = solution_l[:]
                        end_A = datetime.datetime.now()
                        time_spent_a = '搜索时长'+str((end_A - start_A).seconds)+'s'

                        start_B = datetime.datetime.now()
                        board_input_B = copy.deepcopy(mainBoard_r)  # 由于算法限制，此处做一个深拷贝
                        # @TODO 算法B接口
                        solution_r = getPath_astar(board_input_B)
                        revAllMoves_r = solution_r[:]
                        end_B = datetime.datetime.now()
                        time_spent_b = '搜索时长'+str((end_B - start_B).seconds)+'s'

                        # 多线程
                        slider.thread_move(revAllMoves_l,revAllMoves_r,mainBoard,mainBoard_r,message,msg_l,msg_r,time_spent_a,time_spent_b)

                    elif SOLVE_RECT.collidepoint(event.pos):
                        message = "人机对战ing"
                        textSurf, textRect = slider.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
                        slider.screen.blit(textSurf, textRect)

                        msg_l = "AI机器人"
                        msg_r = "人类玩家"
                        message_result_l, message_result_r = 'AI机器人胜利！','人类玩家胜利！'

                        # AI
                        start = datetime.datetime.now()
                        board_input = copy.deepcopy(mainBoard)   # 由于算法限制，此处做一个深拷贝
                        solution_l = getPath_astar(board_input)   # AI算法接口
                        revAllMoves_l = solution_l[:]
                        end = datetime.datetime.now()
                        time_spent = '搜索时长'+str((end - start).seconds)+'s'

                        # 人类玩家
                        # solution_r = solutionSeq + allMoves_r
                        # revAllMoves_r = solution_r[:]
                        pygame.event.clear()
                        while (len(revAllMoves_l)>0):
                            events = pygame.event.poll()
                            slideTo_= None
                            if events.type == KEYUP:
                                if events.key in (K_LEFT, K_a) and gf.isValidMove(mainBoard_r, LEFT):
                                    slideTo_ = RIGHT
                                elif events.key in (K_RIGHT, K_d) and gf.isValidMove(mainBoard_r, RIGHT):
                                    slideTo_ = LEFT
                                elif events.key in (K_UP, K_w) and gf.isValidMove(mainBoard_r, UP):
                                    slideTo_ = DOWN
                                elif events.key in (K_DOWN, K_s) and gf.isValidMove(mainBoard_r, DOWN):
                                    slideTo_ = UP
                            if slideTo_:
                                revAllMoves_l_ = []
                                revAllMoves_r_ = []
                                revAllMoves_r_.append(slideTo_)
                                revAllMoves_l_.append(revAllMoves_l.pop())
                                slider.thread_move(revAllMoves_l_, revAllMoves_r_, mainBoard, mainBoard_r, message, msg_l,msg_r, time_spent)

                        # 多线程
                        # slider.thread_move(revAllMoves_l,revAllMoves_r,mainBoard,mainBoard_r,message,msg_l,msg_r,time_spent)

            # 更新状态并绘图
            if slideTo or slideTo_r:
                slider.slideAnimation(mainBoard, mainBoard_r, slideTo, slideTo_r, '点击按键滑动窗口', animationSpeed)
                gf.makeMove(mainBoard, slideTo)
                gf.makeMove(mainBoard_r, slideTo_r)
                if slideTo != None:
                    allMoves.append(slideTo)  # 记录左侧的历史移动
                if slideTo_r != None:
                    allMoves_r.append(slideTo_r)  # 记录右侧的历史移动

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# if __name__ == '__main__':
#     run_main()