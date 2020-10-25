import pygame,sys
import game_function as gf
from settings import *


class Draw():
    """包含所有的绘画操作类"""
    def __init__(self,screen,FONT,FPS_CLOCK):
        self.screen = screen
        self.FONT = FONT
        self.FPS_CLOCK = FPS_CLOCK

    def make_text(self,text,color,bg_color,left,top):
        '''创建字体对象'''
        text_surf=self.FONT.render(text,True,color,bg_color) #创建文本（抗锯齿）
        #定位文字矩形块
        text_rect=text_surf.get_rect()
        text_rect.topleft=(left,top)
        return (text_surf,text_rect)

    def draw_tile(self,tile_x,tile_y,number, adjx=0, adjy=0):
        '''绘制单个滑块'''
        left_l,top_l= gf.get_left_top_of_tile_l(tile_x, tile_y)
        left_r, top_r = gf.get_left_top_of_tile_r(tile_x, tile_y)
        # 加载贴片图像
        picture_src = "image/image" + str(number) + ".jpeg"
        image = pygame.image.load(picture_src)
        image_rect_l = image.get_rect()
        image_rect_r = image.get_rect()
        image_rect_l.topleft = (left_l + adjx, top_l + adjy)
        image_rect_r.topleft = (left_r + adjx, top_r + adjy)
        self.screen.blit(image,image_rect_l)
        self.screen.blit(image,image_rect_r)

    def make_button_obj(self):
        '''生成按钮文本对象'''
        # 按钮位置
        button_left = WINDOW_WIDTH-120
        button_top = WINDOW_HEIGHT-90
        reset_surf,reset_rect=self.make_text('重置',TEXT_COLOR,BG_COLOR,button_left,button_top)
        new_surf, new_rect = self.make_text('再来一局', TEXT_COLOR, BG_COLOR, button_left, button_top+30)
        solve_surf, solve_rect = self.make_text('AI', TEXT_COLOR, BG_COLOR, button_left, button_top + 60)
        return (reset_surf, reset_rect,new_surf, new_rect,solve_surf, solve_rect)

    def draw_board(self,board,message):
        '''绘制画板'''
        self.screen.fill(BG_COLOR)#添加背景
        if message: #如果有提示信息显示提示信息
            text_surf,text_rect=self.make_text(message,MESSAGE_COLOR,BG_COLOR,5,5) #获取文本对象和定位对象
            self.screen.blit(text_surf,text_rect) #显示消息
        for tile_x in range(BOARD_SIZE): #绘制数字滑块
            for tile_y in range(BOARD_SIZE):
                if board[tile_x][tile_y]:
                    self.draw_tile(tile_x, tile_y, board[tile_x][tile_y])
        #绘制边框
        left_l, top_l= gf.get_left_top_of_tile_l(0, 0)
        left_r, top_r = gf.get_left_top_of_tile_r(0, 0)
        width=BOARD_SIZE*TILE_SIZE
        height=BOARD_SIZE*TILE_SIZE
        pygame.draw.rect(self.screen,BORDER_COLOR,(left_l-5,top_l-5,width+11,height+11),4)
        pygame.draw.rect(self.screen, BORDER_COLOR, (left_r - 5, top_r - 5, width + 11, height + 11), 4)
        #绘制按钮
        reset_surf, reset_rect,new_surf, new_rect,solve_surf, solve_rect=self.make_button_obj()
        self.screen.blit(reset_surf,reset_rect)
        self.screen.blit(new_surf, new_rect)
        self.screen.blit(solve_surf, solve_rect)

    def slide_animation(self, board, direction, message, animation_speed):
        '''绘制滑动动画'''
        blank_x, blank_y = gf.get_blank_index(board)
        # 根据空白坐标和移动方位获取要移动方块的坐标
        # move_x, move_y = 0, 0
        if direction == UP:
            move_x, move_y = blank_x, blank_y + 1
        elif direction == DOWN:
            move_x, move_y = blank_x, blank_y - 1
        elif direction == LEFT:
            move_x, move_y = blank_x + 1, blank_y
        elif direction == RIGHT:
            move_x, move_y = blank_x - 1, blank_y

        self.draw_board(board, message)  # 更新message信息
        base_surf = self.screen.copy()  # 复制一个新的窗口对象(只是单纯的复制）
        move_left_r, move_top_r = gf.get_left_top_of_tile_r(move_x,move_y)
        move_left_l, move_top_l = gf.get_left_top_of_tile_l(move_x, move_y)
        # 先更新空白方块再跟新另一个滑块
        # 绘制空白区(这时候有2块空白区域)
        pygame.draw.rect(base_surf, BG_COLOR, (move_left_l, move_top_l, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(base_surf, BG_COLOR, (move_left_r, move_top_r, TILE_SIZE, TILE_SIZE))
        # 绘制滑动效果
        for i in range(0, TILE_SIZE+1, animation_speed):  # animation_speed步长偏移速度,每次循环后方块的位置向指定方向移动
            self.screen.blit(base_surf, (0, 0))
            ##################################有BUG#######################################################
            if direction == UP:
                self.draw_tile(move_x, move_y, board[move_x][move_y], 0, -i)  # x不动,y轴向上偏移
            if direction == DOWN:
                self.draw_tile(move_x, move_y, board[move_x][move_y], 0, i)  # x不动,y轴向下偏移
            if direction == LEFT:
                self.draw_tile(move_x, move_y, board[move_x][move_y], -i, 0)  # x不动,y轴向左偏移
            if direction == RIGHT:
                self.draw_tile(move_x, move_y, board[move_x][move_y], i, 0)  # x不动,y轴向右偏移
            pygame.display.update()
            self.FPS_CLOCK.tick(FPS)

    def generate_new_puzzle(self,num_slides):
        '''随机初始化，得到初始状态'''
        sequence=[] #移动数据
        board=gf.get_start_board()
        self.draw_board(board, '')  #显示开始画板
        pygame.display.update()
        pygame.time.wait(1000) #等待1000毫秒
        last_move=None
        for i in range(num_slides): #执行移动打乱游戏数据
            move=gf.get_random_move(board,last_move) #获取随机移动方向
            self.slide_animation(board,move,'正在准备游戏....',animation_speed=SPEED_MOVE) #执行移动动画
            gf.make_move(board,move) #数据坐标移动
            sequence.append(move) #记录移动信息
            last_move=move
        return (board,sequence)

    def reset_animation(self, board, all_moves):
        '''重置步骤'''
        rev_all_moves = all_moves[:]
        if rev_all_moves:
            rev_all_moves.reverse()  # 翻转操作列表
            opposite_move = DOWN
            for move in rev_all_moves:  # 反转移动方向,反向移动重置
                if move == UP:
                    opposite_move = DOWN
                if move == DOWN:
                    opposite_move = UP
                if move == LEFT:
                    opposite_move = RIGHT
                if move == RIGHT:
                    opposite_move = LEFT
                self.slide_animation(board, opposite_move, '', animation_speed=SPEED_MOVE)  # 执行移动动画
                gf.make_move(board, opposite_move)  # 数据移动方块