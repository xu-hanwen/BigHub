#深度搜索解决八数码问题

import numpy as np
import copy
import time

MAXD=15	#最大深度                                                    **********


#节点类
class State:
    def __init__(self, state,deep=0,directFlag=None,parent=None,):
    	self.state = state
    	#state用numpy3x3二维数组表示
    	self.deep=deep	#当前节点深度
    	self.direction=['up','down','left','right']
    	#表示空格可以移动的方向
    	if directFlag:
    		self.direction.remove(directFlag)
    	self.parent=parent	#父节点
    	self.blank=0		#空格位

    def getDirection(self):
    	return self.direction

    def printState(self):
        for x in range(4):                                     #********
            for y in range(4):                                 #********
                print(self.state[x,y],end=' ')
            print('')
        print('----->')
        return

    def getBlankPos(self):
    	#返回空格位置
    	pos=np.where(self.state == self.blank)
    	return pos

    def getSubStates(self):
    	#返回扩展得到的节点
    	if not self.direction:
    		return []
    		#上下左右都没得扩展，返回空列表
    	subStates=[]
    	border=len(self.state)-1 #边界

    	row, col=self.getBlankPos()
    	if 'up' in self.direction and  row>0:
    		#空格向上移
    		st=copy.deepcopy(self.state)
    		temp =copy.deepcopy(st)
    		st[row,col],st[row-1,col]=st[row-1,col],temp[row,col]
    		newState=State(st,deep=self.deep+1,directFlag='down',parent=self)
    		#防止子节点向下移动造成重复
    		subStates.append(newState)
    	if 'down' in self.direction and row<border:
    		#空格向下移
    		st=copy.deepcopy(self.state)
    		temp =copy.deepcopy(st)
    		st[row,col],st[row+1,col]=st[row+1,col],temp[row,col]
    		newState=State(st,deep=self.deep+1,directFlag='up',parent=self)
    		#防止子节点向上移动造成重复
    		subStates.append(newState)
    	if 'left' in self.direction and col>0:
     		#空格向左移
    		st=copy.deepcopy(self.state)
    		temp =copy.deepcopy(st)
    		st[row,col],st[row,col-1]=st[row,col-1],temp[row,col]
    		newState=State(st,deep=self.deep+1,directFlag='right',parent=self)  	
    		subStates.append(newState)
    	if 'right' in self.direction and col<border:
     		#空格向右移
    		st=copy.deepcopy(self.state)
    		temp =copy.deepcopy(st)
    		st[row,col],st[row,col+1]=st[row,col+1],temp[row,col]
    		newState=State(st,deep=self.deep+1,directFlag='left',parent=self)  	
    		subStates.append(newState)

    	return subStates

    def DFS(self,startState):
    	openTable=[]
    	closeTable=[]
    	expandnum=0    	

    	openTable.append(self)

    	steps=0
    	#开始循环
    	while len(openTable)>0 :
    		#open()为空则搜索失败
    		n=openTable.pop()
    		closeTable.append(n)
    		#remove(n,open()), add(n,close())
    		subStates=n.getSubStates()
    		#扩展节点n
    		path=[]
    		solution = []
    		for sub in subStates:
    			if(sub.state == sub.goalState).all():
    				#all()用于判断所有位置是否正确
    				#如果到达目标节点，返回路径
    				while sub.parent and sub.parent != startState:
    					solution.append(getOperate(sub.state,sub.parent.state))
    					path.append(sub.parent)
    					sub=sub.parent
    				path.reverse()
    				return path,solution,steps+1,expandnum
    		if subStates[0].deep<MAXD:
                #同一层节点扩展出来的子节点的深度是一样的
    		    openTable.extend(subStates)
    		if subStates[0].deep==MAXD:
    		    expandnum-=1    		    

    		steps+=1
    		expandnum+=1
    	else:
    		return None,None,None,None


def DFS_main(start,goal):

    #字符串转列表
    strlist=list(start)
    numlist=[int(x) for x in strlist]
    
    glist=list(goal)
    goallist=[int(x) for x in glist]   

    #初始节点
    startState=State(np.array(numlist).reshape(4,4))                     #********
    #目标节点 
    State.goalState=np.array(np.array(goallist).reshape(4,4))            #********
            
    s1 = State(state=startState.state)
    path, solution, steps,expandnum = s1.DFS(startState)

    if path:
        return expandnum, steps, solution
    else:
        return None,None,None


def getOperate(s,p):
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

def getPath(state):
    goal = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 0]
    statelist = []
    for l in state:
        statelist.extend(l)
    for i in range(len(statelist)):
        if statelist[i] == None:
            statelist[i] = 0

    expandnum, steps, solution = DFS_main(statelist,goal)

    return solution


if __name__ == '__main__':
    sta=[[0, 1, 10, 9, 2, 5, 6, 13, 3, 7, 15, 14, 4, 8, 11, 12]]                                                    #*******
    end=[1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 0]
    starttime = time.time()

    solution=getPath(sta)
    endtime = time.time()
    print(solution)
    print('Running time: %s Seconds' % (endtime - starttime))



