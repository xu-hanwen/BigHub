import pygame,sys,os
from draw import Draw
from settings import *
import game_function as gf
from picture import image
from A算法 import main_A


def run_game():
    # 初始化并创建屏幕
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("数码难")

    # 界面设计
    # 创建字体对象（字体类型和大小）
    FONT = pygame.font.Font("C:\Windows\Fonts\simsun.ttc", FONT_SIZE)
    draw = Draw(screen, FONT, FPSCLOCK)
    board_now,solutionSeq = draw.generate_new_puzzle(20)
    # main_A(board_now)
    # print(board_now)
    board_gloal = gf.get_start_board()
    allmoves = []

    while True:
        slideTo = None
        msg = '点击按键滑动窗口'
        if board_now == board_gloal:
            msg = '游戏结束'

        draw.draw_board(board_now, msg)

        for event in pygame.event.get():
            # 检测退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # check_mousebuttonup(draw,event,board_now,allmoves,solutionSeq)
                spotx, spoty = gf.get_spot_clicked(board_now, event.pos[0], event.pos[1])
                reset_surf, reset_rect, new_surf, new_rect, solve_surf, solve_rect = draw.make_button_obj()
                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if reset_rect.collidepoint(event.pos):
                        draw.reset_animation(board_now, allmoves)  # clicked on Reset button
                        allmoves = []
                    elif new_rect.collidepoint(event.pos):
                        board_now, solutionSeq = draw.generate_new_puzzle(20)  # clicked on New Game button
                        allmoves = []
                    elif solve_rect.collidepoint(event.pos):
                        draw.reset_animation(board_now, solutionSeq + allmoves)  # clicked on Solve button
                        allmoves = []
                else:
                    blankx, blanky = gf.get_blank_index(board_now)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
            elif event.type == pygame.KEYUP:
                # gf.check_keyup_events(event,board_now)
                if event.key in (pygame.K_LEFT, pygame.K_a) and gf.is_valid_move(board_now, LEFT):
                    slideTo = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and gf.is_valid_move(board_now, RIGHT):
                    slideTo = RIGHT
                elif event.key in (pygame.K_UP, pygame.K_w) and gf.is_valid_move(board_now, UP):
                    slideTo = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and gf.is_valid_move(board_now, DOWN):
                    slideTo = DOWN
            if slideTo:
                draw.slide_animation(board_now,slideTo,'点击按键滑动窗口',SPEED_MOVE)
                gf.make_move(board_now,slideTo)
                allmoves.append(slideTo)
            pygame.display.update()
            FPSCLOCK.tick(FPS)


# if __name__ == "__main__":
#     # src = input("请输入图片文件路径：")
#     # if os.path.isfile(src):
#     #     dstpath = input("请输入图片输出目录(不输入路径则表示使用源图片所在目录)：")
#     #     image(src,dstpath)
#     #     run_game()
#     # else:
#     #     print('图片文件%s不存在!' % src)
#
#     run_game()
