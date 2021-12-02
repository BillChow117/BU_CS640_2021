import time
import numpy as np
import math
from NetworkManager import NetworkManager
from EnvironmentState import State


RES_COL = 400
RES_ROW = 300

LEFT = bytes.fromhex('00')
UP = bytes.fromhex('01')
RIGHT =  bytes.fromhex('02')
DOWN =  bytes.fromhex('03')
NOOP =  bytes.fromhex('04')

def distanceSquare(p1,p2,crossWall = True):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]

    dx = x2 - x1
    dy = y2 - y1
    
    if not crossWall:
        return dx**2 + dy**2

    if abs(dx) <= RES_COL/2 and abs(dy) <= RES_ROW/2:
        return dx**2 + dy**2
    elif abs(dx) <= RES_COL/2 and abs(dy) > RES_ROW/2:
        return dx**2 + (RES_ROW-dy)**2
    elif abs(dx) > RES_COL/2 and abs(dy) <= RES_ROW/2:
        return (RES_COL-dx)**2 + dy**2
    else:
        return (RES_COL-dx)**2 + (RES_ROW-dy)**2

def distance(p1,p2,crossWall = True):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if not crossWall:
        return dx + dy

    if dx <= RES_COL/2 and dy <= RES_ROW/2:
        return dx + dy
    elif dx <= RES_COL/2 and dy > RES_ROW/2:
        return dx + RES_ROW - dy
    elif dx > RES_COL/2 and dy <= RES_ROW/2:
        return RES_COL - dx + dy
    else:
        return RES_COL - dx + RES_ROW - dy

def getStates(currentState:State,opMap):
    head= np.array([currentState.body[0].x1,currentState.body[0].y1])
    return [head+opMap[op] for op in opMap.keys()]

def collisionDetection(point,body,width = 0):
    x,y = point
    for line in body:
        x1,y1,x2,y2 = line.x1,line.y1,line.x2,line.y2
        if x1 == x2 and x1 - width <= x <= x1 + width:
            if y1 < y2:
                if y1 - width <= y <= y2 + width:
                    return True
            elif y2 - width <= y <= y1 + width:
                return True
        elif y1 == y2 and y1 - width <= y <= y2 + width:
            if x1 < x2:
                if x1 - width <= x <= x2 + width:
                    return True
            elif x2 - width <= x <= x1 + width:
                return True
    return False
            

class Controller:
    
    def __init__(self,ip='localhost',port=4668):
        #Do not Modify
        self.networkMgr=NetworkManager()
        State.col_dim,State.row_dim=self.networkMgr.initiateConnection(ip,port) # Initialize network manager and set environment dimensions
        self.state=State() # Initialize empty state
        self.myInit() # Initialize custom variables
        pass

    #define your variables here
    def myInit(self):
        #TODO
        self.opMap={LEFT:[-1,0],RIGHT:[1,0],UP:[0,-1],DOWN:[0,1]}
        self.ops=list(self.opMap.keys())
        self.step = 0
        self.stepQueue = []
        pass
    
    #Returns next command selected by the agent.
    def getNextCommand(self):
        #TODO Implement an Intelligent agent that plays the game
        # Hint You will require a collision detection function.
        food=list(self.state.food)
        states=getStates(self.state,self.opMap)
        cost = []
        for head in states:
            if not collisionDetection(head,self.state.body,0):
                cost.append(distance(food,head))
            else:
                cost.append(math.inf)
        order = np.argmin(cost)
        return self.ops[order]

    def control(self):
        #Do not modify the order of operations.
        # Get current state, check exit condition and send next command.
        while(True):
            # 1. Get current state information from the server
            self.state.setState(self.networkMgr.getStateInfo())
            # 2. Check Exit condition
            if self.state.food==None:
                break
            # 3. Send next command
            self.step+=1
            # print(self.step)
            self.networkMgr.sendCommand(self.getNextCommand())


cntrl=Controller()
cntrl.control()