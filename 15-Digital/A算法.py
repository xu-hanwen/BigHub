import numpy as np
import copy
import time


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

    def getDirection(self):
        return self.direction

    def printState(self):
        for x in range(4):  # ********
            for y in range(4):  # ********
                print(self.state[x, y], end=' ')
            print('')
        print('----->')
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
            news.hn = news.h(goal)
            news.gn = gn
            news.fn = news.gn + news.hn
            subStates.append(news)

        return subStates

    def h(self, goal):
        self.hn = 0
        for x in range(4):
            for y in range(4):
                if self.state[x, y] != goal.state[x, y]:
                    self.hn += 1
        return self.hn



def solve(start, goal):

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

        # 添加到closeTable中
        closeTable.append(node)

        # 扩展表
        subStates = node.generateSubStates(goal)

        #检验是否得到结果
        for s in subStates:
            if (s.state == goal.state).all():
                # 如果目标节点可达，返回可达路径
                path = []
                while s.parent and s.parent != start:
                    path.append(s.parent)
                    s = s.parent
                path.reverse()
                return path, steps + 1, ExpandNode

        openTable.extend(subStates)
        ExpandNode = steps - (steps - len(openTable)) + 1
        steps += 1
        if (steps > 100000):
            return None, None, None
    return None, None, None


def main_A(start):
    # start = [15,0,2,3,4,1,6,7,8,5,9,14,12,13,11,10]
    # [[None, 5, 9, 13], [1, 2, 6, 14], [3, 7, 10, 12], [4, 8, 15, 11]]
    # start = [5, 1, 2, 4, 9, 6, 3, 8, 13, 15, 10, 11, 14, 0, 7, 12]  # *******
    goal = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, None]
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

    # 路径，步数，  扩展节点数
    path, steps, expandnum = solve(s1, goalState)
    # 如果需要输出找到的路径
    if path:  # if find the solution
        for node in path:
            # print the path from the origin to final state
            node.printState()
        print(goalState.state)

    endtime = time.time()

    print('扩展节点数：', expandnum, '   步数：', steps)
    print('Running time: %s Seconds' % (endtime - starttime))

# main_A(start = [5, 1, 2, 4, 9, 6, 3, 8, 13, 15, 10, 11, 14, 0, 7, 12])