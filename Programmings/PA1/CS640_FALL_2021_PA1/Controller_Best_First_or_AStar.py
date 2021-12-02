import cProfile
from os import close
import time
from collections import deque
import numpy as np
import math
from NetworkManager import NetworkManager
from EnvironmentState import State


RES_COL = 400
RES_ROW = 300

path_count = 0

LEFT = bytes.fromhex('00')
UP = bytes.fromhex('01')
RIGHT =  bytes.fromhex('02')
DOWN =  bytes.fromhex('03')
NOOP =  bytes.fromhex('04')

# Class of Point
class Point:

    def __init__(self,coords,parent = None, basecost = math.inf, targetcost = math.inf):
        """
        Coords(tuple): Coordinates of the point. Like (3,5)
        Parents(Point): Where the path come from.
        BaseCost: Distance from the start point to this point
        TargetCost: Distance from the target point to this point
        TotalCost: Sum of two distances above, for the convenience when to choose the point to explore
        """
        self.Coords = coords
        self.Parent = parent
        self.BaseCost = basecost
        self.TargetCost = targetcost
        self.TotalCost = self.BaseCost + self.TargetCost
        pass
    
    # function to change base cost, update total cost simultaneously
    def setBaseCost(self,basecost):
        self.BaseCost = basecost
        self.TotalCost = self.BaseCost + self.TargetCost

    # function to change target cost, update total cost simultaneously
    def setTargetCost(self,targetcost):
        self.TargetCost = targetcost
        self.TotalCost = self.BaseCost + self.TargetCost

# Algorithm class of best-first search or A star search
class Best_First_or_AStar:

    def __init__(self,map_col,map_row,state):
        """
        step_stack(list): The stack to store each operations in the path
        col: The col of the map
        row: The row of the map
        state: Game information of Snake Classic
        head(Point): Head point of the snake
        target(Point): Food point
        open_set(list): Set of points to access
        close_set(list): Set of points accessed
        set_map(array): Store the status of each point whether in open set(1), close set(-1) or undesided(0), to accelerate isInOpenSet() and isInCloseSet()
        reverseOpmMap(map): Store all operation that the snake can do
        """
        self.step_stack = []
        self.col = map_col
        self.row = map_row
        self.state = state
        self.head = Point((self.state.body[0].x1,self.state.body[0].y1))
        self.target = Point(self.state.food)
        self.open_set = []
        self.close_set = []
        self.set_map = np.zeros((self.col,self.row))
        self.reverseOpMap={(-1,0):LEFT,(1,0):RIGHT,(0,-1):UP,(0,1):DOWN}
        pass

    # set a point in open set
    def moveInOpen(self,p:Point):
        self.set_map[p.Coords[0]][p.Coords[1]] = 1

    # set a point in close set
    def moveInClose(self,p:Point):
        self.set_map[p.Coords[0]][p.Coords[1]] = -1

    # return infinit if a point is on the snake body
    def collisionDetection(self,point):
        #avoid the snake eating itself
        x,y = point
        for line in self.state.body:
            x1,y1,x2,y2 = line.x1,line.y1,line.x2,line.y2
            if x1 == x2 and x1 == x:            # vertical line
                if y1 < y2:
                    if y1 <= y <= y2:
                        return math.inf
                elif y2 <= y <= y1:
                    return math.inf
            elif y1 == y2 and y1 == y :         # horizontal line
                if x1 < x2:
                    if x1 <= x <= x2:
                        return math.inf
                elif x2 <= x <= x1:
                    return math.inf
        return 0

    # return the Manhattan distance of two point
    def distanceManhattan(self,p1:Point,p2:Point):
        x1,y1 = p1.Coords
        x2,y2 = p2.Coords

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # this line disable telepotation function
        #return dx + dy

        if dx <= self.col/2 and dy <= self.row/2:
            return dx + dy
        elif dx <= self.col/2 and dy > self.row/2:
            return dx + self.row - dy
        elif dx > self.col/2 and dy <= self.row/2:
            return self.col - dx + dy
        else:
            return self.col - dx + self.row - dy

    # return the Euclid distance of two point
    def distanceEuclid(self,p1:Point,p2:Point):
        x1,y1 = p1.Coords
        x2,y2 = p2.Coords

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # this line disable telepotation function
        #return math.sqrt(dx**2 + dy**2)

        if dx <= self.col/2 and dy <= self.row/2:
            return math.sqrt(dx**2 + dy**2)
        elif dx <= self.col/2 and dy > self.row/2:
            return math.sqrt(dx**2 + (self.row-dy)**2)
        elif dx > self.col/2 and dy <= self.row/2:
            return math.sqrt((self.col-dx)**2 + dy**2)
        else:
            return math.sqrt((self.col-dx)**2 + (self.row-dy)**2)

    # return the distance between the point and the head
    def baseDistance(self,p:Point):
        #this line enable A star algorithm
        #return self.distanceManhattan(self.head,p) 

        #this line enable best-first algorithm
        return 0

    # return the distance between the point and the target
    def targetDistance(self,p:Point):
        return 2 * self.distanceManhattan(self.target,p) + self.collisionDetection(p.Coords)

    # return whether a point is in the open set
    def isInOpenSet(self,p:Point):
        return self.set_map[p.Coords[0]][p.Coords[1]] == 1

    # return whether a point is in the open set
    def isInCloseSet(self,p:Point):
        return self.set_map[p.Coords[0]][p.Coords[1]] == -1

    # to find the lowest total cost point in the open set
    def getIndexofMinCostPointINOpenSet(self):
        index = 0
        select = -1
        min = math.inf
        for p in self.open_set:
            cost = p.TotalCost
            if cost < min:
                min = cost
                select = index
            index += 1
        return select

    # add the coordinates of two point
    def addCoords(self,c1,c2):
        x = (c1[0] + c2[0]) % self.col
        y = (c1[1] + c2[1]) % self.row
        return (x,y)
    
    # find the operation between two adjacent point
    def getOp(self,c1,c2):
        for key in self.reverseOpMap.keys():
            if self.addCoords(c1,key) == c2:
                return key

    # find all points to explore of current point p
    def explore(self,p:Point):
        Output = []
        for op in self.reverseOpMap.keys():
            coords = self.addCoords(p.Coords,op)
            Output.append(Point(coords))
        return Output

    # whether a point is head
    def isHead(self,p:Point):
        if p.Coords[0] == self.head.Coords[0] and p.Coords[1] == self.head.Coords[1]:
            return True
        else:
            return False

    # whether a point is target, the food
    def isTarget(self,p:Point):
        if p.Coords[0] == self.target.Coords[0] and p.Coords[1] == self.target.Coords[1]:
            return True
        else:
            return False

    # get all operations from target to head
    def getSteps(self,p:Point):
        curr = p
        parent = curr.Parent
        while(parent != None):
            ops = self.reverseOpMap[self.getOp(parent.Coords,curr.Coords)]
            if isinstance(ops,list):
                self.step_stack.extend(ops)
            else:
                self.step_stack.append(ops)
            #self.step_stack.append(self.reverseOpMap[self.getOp(parent.Coords,curr.Coords)])
            curr = parent
            parent = curr.Parent

    # return the length of the last line of the body
    def getTailLength(self):
        x1,y1,x2,y2 = self.state.body[-1].x1,self.state.body[-1].y1,self.state.body[-1].x2,self.state.body[-1].y2
        if x1 == x2:
            return 20 if 20 > abs(y2 - y1) else abs(y2 - y1)
        else:
            return 20 if 20 > abs(x2 - x1) else abs(x2 - x1)

    # the search algorithm
    def search(self):
        # initial head point and put in the open set
        self.head.setBaseCost(0)
        self.head.setTargetCost(0)
        self.open_set.append(self.head)
        self.moveInOpen(self.head)

        # when open set is not empty
        while(len(self.open_set) != 0):
            # find the point with lowest total cost
            index = self.getIndexofMinCostPointINOpenSet()
            curr_Point = self.open_set[index]

            # current point is target or already have more step than the tail
            if self.isTarget(curr_Point) or curr_Point.BaseCost >= self.getTailLength():
                # return the found path
                self.getSteps(curr_Point)
                break
            else:
                # remove current point from open set and put it in close set
                self.open_set.pop(index)
                self.close_set.append(curr_Point)
                self.moveInClose(curr_Point)
                
                # get all adjacent points of current point
                available_List = self.explore(curr_Point)
                for point in available_List:
                    # the point is in close set (accessed)
                    if self.isInCloseSet(point):
                        continue
                    # not in either close set or open set
                    elif not self.isInOpenSet(point):
                        # set its parent is current point
                        point.Parent = curr_Point
                        # calculate bast cost and target cost
                        point.setBaseCost(self.baseDistance(point))
                        point.setTargetCost(self.targetDistance(point))
                        # put in the open set
                        self.open_set.append(point)
                        self.moveInOpen(point)



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

        #the stack store operations we've got
        self.step_stack = []
        pass
    
    #Returns next command selected by the agent.
    def getNextCommand(self):
        #TODO Implement an Intelligent agent that plays the game
        # Hint You will require a collision detection function.

        while len(self.step_stack) == 0:
            astar = Best_First_or_AStar(RES_COL,RES_ROW,self.state)
            astar.search()
            self.step_stack = astar.step_stack

        command = self.step_stack.pop()
        return command

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
            self.networkMgr.sendCommand(self.getNextCommand())
            #time.sleep(0.004)
    

cntrl=Controller()
cntrl.control()
#cProfile.run("cntrl.control()")
