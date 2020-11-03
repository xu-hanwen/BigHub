# 游戏参数设置
BOARDWIDTH = 4  # 游戏板列数
BOARDHEIGHT = 4 # 游戏板行数
TILESIZE = 80   # 游戏块大小
WINDOWWIDTH = 1280  # 窗口大小
WINDOWHEIGHT = 480
FPS = 30
BLANK = None
animationSpeed = int(TILESIZE / 10)

# 配置颜色
#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)   # 文本颜色
BRIGHTBLUE =    (  0,  50, 255)   # 滑块颜色
DARKTURQUOISE = (  3,  54,  73)   # 背景颜色
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE   
TILECOLOR = BGCOLOR
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20   # 字体大小

BUTTONCOLOR = WHITE               
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
# 窗口边距
XMARGIN = int((WINDOWWIDTH/2 - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
XMARGIN_r = XMARGIN + int(WINDOWWIDTH/2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# 动作配置
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'



