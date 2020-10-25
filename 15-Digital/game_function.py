import pygame,random
from settings import *

def get_start_board():
    """生成目标状态"""
    # board = [[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,None]]
    board = []
    for x in range(BOARD_SIZE):
        conter = 1+x  # 在此记录第一行数字信息
        column = []   # 记录y轴数字信息
        for y in range(BOARD_SIZE):
            column.append(conter)
            conter += BOARD_SIZE  # 在此记录每一列中的数字
        board.append(column)
    board[BOARD_SIZE-1][BOARD_SIZE-1] = None  # 最后一个滑块是空的
    return board

def get_blank_index(board):
    """返回空白滑块的索引"""
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == None:
                return (x,y)

def make_move(board,move):
    """滑块数值更新"""
    blank_x,blank_y = get_blank_index(board)
    if move == UP:
        board[blank_x][blank_y],board[blank_x][blank_y+1]=board[blank_x][blank_y+1],board[blank_x][blank_y]
    elif move == DOWN:
        board[blank_x][blank_y], board[blank_x][blank_y - 1] = board[blank_x][blank_y - 1], board[blank_x][blank_y]
    elif move == LEFT:
        board[blank_x][blank_y], board[blank_x + 1][blank_y] = board[blank_x + 1][blank_y], board[blank_x][blank_y]
    elif move == RIGHT:
        board[blank_x][blank_y], board[blank_x - 1][blank_y] = board[blank_x - 1][blank_y], board[blank_x][blank_y]

def is_valid_move(board,move):
    """移动合法性判断"""
    blank_x,blank_y = get_blank_index(board)
    return (move == UP and blank_y!=BOARD_SIZE-1) \
           or (move == DOWN and blank_y !=0)  \
           or (move == LEFT and blank_x != BOARD_SIZE - 1) \
           or (move == RIGHT and blank_x != 0)

def get_random_move(board,last_move=None):
    """滑块随机移动"""
    vaild_moves=[UP,DOWN,LEFT,RIGHT]
    # 移动方向筛选(排除相邻两次上下、左右移动和不合法移动）
    if last_move == UP or not is_valid_move(board,DOWN):
        vaild_moves.remove(DOWN)
    if last_move == DOWN or not is_valid_move(board,UP):
        vaild_moves.remove(UP)
    if last_move == LEFT or not is_valid_move(board, RIGHT):  # 排除左右重复移动和向右不能移动选项
        vaild_moves.remove(RIGHT)
    if last_move == RIGHT or not is_valid_move(board, LEFT):
        vaild_moves.remove(LEFT)
    return random.choice(vaild_moves)

def get_left_top_of_tile_l(tile_x,tile_y):
    """根据滑块索引返回其像素缩值"""
    left = X_MARGIN_l + (tile_x * TILE_SIZE) + (tile_x - 1)
    top  = Y_MARGIN + (tile_y*TILE_SIZE) + (tile_y-1)
    return (left,top)

def get_left_top_of_tile_r(tile_x,tile_y):
    """根据滑块索引返回其像素缩值"""
    left = X_MARGIN_r + (tile_x * TILE_SIZE) + (tile_x - 1)
    top  = Y_MARGIN + (tile_y*TILE_SIZE) + (tile_y-1)
    return (left,top)

def get_spot_clicked(board,x,y):
    '''根据像素坐标找到索引'''
    for tile_x in range(BOARD_SIZE):
        for tile_y in range(BOARD_SIZE):
            left_r,top_r=get_left_top_of_tile_r(tile_x,tile_y)
            left_l,top_l=get_left_top_of_tile_l(tile_x, tile_y)
            tile_rect_l=pygame.Rect(left_l, top_l, TILE_SIZE, TILE_SIZE) #创建坐标矩形
            tile_rect_r=pygame.Rect(left_r, top_r, TILE_SIZE, TILE_SIZE)
            if tile_rect_l.collidepoint(x, y) or tile_rect_r.collidepoint(x,y): #判断像素坐标点是否在矩形内部
                return (tile_x,tile_y) #返回数据坐标
    return (None,None)


