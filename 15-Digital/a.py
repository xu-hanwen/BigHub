# import random
import numpy as np
import time
import copy

class State:
    def __init__(self, state, directionFlag=None, parent=None):
        self.state = state
        # state is a ndarray with a shape(3,3) to storage the state
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
            # record the possible directions to generate the sub-states
        self.parent = parent  # 父节点
        self.symbol = 0
        self.gn = 0
        self.hn = 0
        self.fn = 0

    def h(self, goal):
        self.hn = 0
        for x in range(4):
            for y in range(4):
                if self.state[x, y] != goal.state[x, y]:
                    self.hn += 1
        return self.hn

    def getDirection(self):
        return self.direction

    def printState(self):
        for x in range(4):  # ********
            for y in range(4):  # ********
                print(self.state[x, y], end=' ')
            print('')
        print('goalstate: ')
        return

    def getEmptyPos(self):
        # 返回空格坐标
        postion = np.where(self.state == self.symbol)
        return postion

    def generateSubStates(self, goal):
        # 返回扩展后的节点

        if not self.direction:
            return []
        subStates = []

        boarder = len(self.state) - 1
        # the maximum of the x,y
        row, col = self.getEmptyPos()
        gn = self.gn +1
        if 'left' in self.direction and col > 0:
            # it can move to left
            s = copy.deepcopy(self.state)
            temp = s[row, col]
            s[row, col] = s[row, col - 1]
            s[row, col - 1] = temp
            news = State(s, directionFlag='right', parent=self)
            if len(news.direction) < 3:
                news.direction = ['up', 'down', 'left']
            news.hn = news.h(goal)
            news.gn = gn
            news.fn = news.gn + news.hn
            # 不用再往反方向走回去
            subStates.append(news)
        if 'up' in self.direction and row > 0:
            # it can move to upper place
            s = copy.deepcopy(self.state)
            temp = s[row, col]
            s[row, col] = s[row - 1, col]
            s[row - 1, col] = temp
            news = State(s, directionFlag='down', parent=self)
            if len(news.direction) < 3:
                news.direction = ['up', 'right', 'left']
            news.hn = news.h(goal)
            news.gn = gn
            news.fn = news.gn + news.hn
            subStates.append(news)
        if 'down' in self.direction and row < boarder:  # it can move to down place
            s = copy.deepcopy(self.state)
            temp = s[row, col]
            s[row, col] = s[row + 1, col]
            s[row + 1, col] = temp
            news = State(s, directionFlag='up', parent=self)
            if len(news.direction) < 3:
                news.direction = ['down', 'right', 'left']
            news.hn = news.h(goal)
            news.gn = gn
            news.fn = news.gn + news.hn
            subStates.append(news)
        if 'right' in self.direction and col < boarder:  # it can move to right place
            s = copy.deepcopy(self.state)
            temp = s[row, col]
            s[row, col] = s[row, col + 1]
            s[row, col + 1] = temp
            news = State(s, directionFlag='left', parent=self)
            if len(news.direction) < 3:
                news.direction = ['up', 'down', 'right']
            news.hn = news.h(goal)
            news.gn = gn
            news.fn = news.gn + news.hn
            subStates.append(news)

        return subStates

def Asolve(start, goal):

    ExpandNode = 0
    # generate a empty openTable
    openTable = []
    # generate a empty closeTable
    closeTable = []
    # append the origin state to the openTable

    openTable.append(start)

    steps = 0
    # start the loop
    while len(openTable) > 0:
        # 若openTable为空，则搜索结束

        # remove当前节点
        node = openTable[0]
        fn = node.fn
        hn = node.hn
        for n in openTable:
            if n.fn < fn:
                node = n
                fn = n.fn
                hn = n.hn
            elif n.fn == fn and n.hn < hn:
                node = n
                fn = n.fn
                hn = n.hn

        openTable.remove(node)
        # print(node.state)

        # 添加到closeTable中
        closeTable.append(node)

        # 扩展表
        subStates = node.generateSubStates(goal)

        #检验是否得到结果
        for s in subStates:
            if s.hn == 0:
                # 如果目标节点可达，返回可达路径
                solution = []
                path = [s]
                while s.parent:
                    solution.append(getOperate(s.state, s.parent.state))
                    path.append(s.parent)
                    s = s.parent
                path.reverse()
                return path, solution, steps + 1, ExpandNode

        openTable.extend(subStates)
        ExpandNode = steps - (steps - len(openTable)) + 1
        steps += 1
        if steps > 100000 :
            return None, None, None
    return None, None, None


def getPath(state):
    goal = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 0]
    statelist = []
    for l in state:
        statelist.extend(l)
    for i in range(len(statelist)):
        if statelist[i] == None:
            statelist[i] = 0

    # 初始节点
    originState = State(np.array(statelist).reshape(4, 4))  # **************
    # 目标数组
    goalState = State(np.array(goal).reshape(4, 4))

    s1 = State(state=originState.state)

    # 路径，解决方案，步数，  扩展节点数
    path, solution, steps, expandnum = Asolve(s1, goalState)

    return solution

def getOperate(s, p):
    """
    :param p:父节点
    :param s:子节点
    :return:　0,1,2,3: 上下左右
    """
    i = 0
    j = 0
    for i in range(4):
        for j in range(4):
            if p[i][j] == 0:
                break
        if p[i][j] == 0:
            break
    if i > 0 and s[i - 1][j] == 0:
        return 'left'
    elif i < 3 and s[i + 1][j] == 0:
        return 'right'
    elif j > 0 and s[i][j - 1] == 0:
        return 'up'
    elif j < 3 and s[i][j + 1] == 0:
        return 'down'

if __name__ == '__main__':
    start = [1, 5, 9, 13, 2, 6, 10, 0, 3, 7, 11, 14, 4, 8, 12, 15]
    # random.shuffle(start)
    goal = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 0]
    symbolOfEmpty = 0
    State.symbol = symbolOfEmpty

    starttime = time.time()

    # 字符串转列表
    stalist = list(start)
    numlist = [int(x) for x in stalist]

    glist = list(goal)
    goallist = [int(x) for x in glist]

    # 初始节点
    originState = State(np.array(numlist).reshape(4, 4))  # **************
    # 目标数组
    goalState = State(np.array(goallist).reshape(4, 4))

    s1 = State(state=originState.state)

    # 路径，解决方案，步数，  扩展节点数
    path, solution, steps, expandnum = Asolve(s1, goalState)

    # 如果需要输出找到的路径
    if path:  # if find the solution
        for node in path:
            # print the path from the origin to final state
            node.printState()
        print(goalState.state)
        print(solution)

    endtime = time.time()
    if path:
        print('路径长度：', len(solution))
    print('扩展节点数：', expandnum, '   步数：', steps)
    print('Running time: %s Seconds' % (endtime - starttime))

