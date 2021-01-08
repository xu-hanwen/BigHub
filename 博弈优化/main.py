import random

class Node():
    def __init__(self):
        if (random.random() < 0.5):
            self.state = 'C'
        else:
            self.state = 'D'
        self.value = 0
        self.all_value = 0
        self.neighbour_number = 0
        self.nb = list()

class Net():
    def __init__(self, n):
        self.numbers = n
        self.nodes = list()
        self.edges = list()
        self.reward = 0
        self.initNode()

    def printState(self):
        self.getAllReward()
        print('各节点决策方案及其收益：')
        for i in range(self.numbers):
            print('Noede%d:%c ==> reward: %f ' %
                  (i, self.nodes[i].state, self.nodes[i].value))
        print("网络总回报:", self.reward)

    def initNode(self):
        for _ in range(self.numbers):
            tmp_node = Node()
            self.nodes.append(tmp_node)

    def buideNet(self, es):
        for e in es:
            self.edges.append(e)
        self.updateNb()

    def updateNb(self):
        for a, b in self.edges:
            a.nb.append(self.nodes.index(b))
            b.nb.append(self.nodes.index(a))
        for i in range(self.numbers):
            self.nodes[i].neighbour_number = len(self.nodes[i].nb)

    def calValue(self):
        for i in range(self.numbers):
            self.nodes[i].all_value = 0
        for a, b in self.edges:
            a.all_value += rewardMat[a.state][b.state][0]
            b.all_value += rewardMat[a.state][b.state][1]
        for i in range(self.numbers):
            self.nodes[i].value = self.nodes[i].all_value / \
                self.nodes[i].neighbour_number

    def updateState(self):
        self.calValue()
        flag = False
        for i in range(self.numbers):
            if(self.nodes[i].state == 'C'):
                reward1 = self.getReward(i)
                self.nodes[i].state = 'D'
                reward2 = self.getReward(i)
                if(reward2 <= reward1):
                    self.nodes[i].state = 'C'
                    continue
                flag = True
            elif(self.nodes[i].state == 'D'):
                reward1 = self.getReward(i)
                self.nodes[i].state = 'C'
                reward2 = self.getReward(i)
                if(reward2 <= reward1):
                    self.nodes[i].state = 'D'
                    continue
                flag = True
        return flag

    def getReward(self, i):
        all_value = 0
        for s in self.nodes[i].nb:
            all_value += rewardMat[self.nodes[i].state][self.nodes[s].state][0]
        value = all_value / self.nodes[i].neighbour_number
        return value

    def getAllReward(self):
        for a, b in self.edges:
            self.reward += sum(rewardMat[a.state][b.state])
        return self.reward


r = 0.1
rewardMat = {
    'C': {'C': (1, 1), 'D': (1-r, 1+r)},
    'D': {'C': (1+r, 1-r), 'D': (0, 0)}
}
net = Net(20)
edge_list = [(0, 1), (0, 2), (2, 3), (2, 4),
                (3, 15), (4, 14), (4, 5),
                (5, 6), (6, 19), (7, 17),
                (8, 15), (6, 11), (9, 10),
                (0, 16), (12, 16), (12, 19),
                (13, 15), (14, 18), (17, 19)
                ]

net.buideNet(({net.nodes[a], net.nodes[b]} for a, b in edge_list))

# 循环更新节点状态，直至每个人都不愿改变自己的决策
while net.updateState():
    continue
net.printState()