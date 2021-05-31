import time
from collections import namedtuple
from MAF_Utility import Direction
from collections import deque
import random as rand

_Surrounding = namedtuple("_Surrounding",("forward","right","backward","left"))
# __name__ = "__main__"


class Position():

    def __init__(self, xval=0, zval=0):
        self._x = xval
        self._z = zval

    def addx(self, add=1):
        """+1 to x, or value"""
        self._x += add

    def subx(self, sub=1):
        """-1 to x, or value"""
        self._x -= sub

    def addz(self, add=1):
        """+1 to z, or value"""
        self._z += add

    def subz(self, sub=1):
        """-1 to z, or value"""
        self._z -= sub

    @property
    def getx(self):
        return self._x

    @property
    def getz(self):
        return self._z

    def x(self, value):
        """Set x to value"""
        self._x = value

    def z(self, value):
        """Set x to value"""
        self._z = value

    def __str__(self):
        return "x: " + str(self._x) + " z: " + str(self._z)


class FurnitureAgent:

    def __init__(self, floorplans):
        self.floorplans = floorplans
        self.position = Position()
        self.level = 0
        self.direction = None
        self.savedblock =[]
        self.setup()
        self.nextlevelstartingdirection = Direction.NONE
        self.nextlevelstartingpos = Position()
        self.placementqueue = deque()
        self.clockwise = True
        self.furperlevel=0
        self.furnitures = self._getfurniture()
        self.furniturepos = []


        # self._getfurniture()

    def Act(self):

        steps = 0
        while True:
            if len(self.placementqueue) > 0:
                self.UpdateBlock(self.placementqueue.popleft())
            # print("Current Direction: " + str(self.direction))

            surrondingobjects = self._getsurroundingobjects()

            if surrondingobjects.forward == "N":
                self.UpdateBlock("WA")
                self.placementqueue.append("WA")
            if surrondingobjects.left in ["0","E"] :
                self.turnleft()
                surrondingobjects = self._getsurroundingobjects()
            if len(surrondingobjects.left) > 3 and surrondingobjects.left[3] == "4":  # when fidning top staris, prepare for nextlevel
                self.getdirectionnextlevel(surrondingobjects.left[2])
                self.nextlevelstartingpos = self.getleftposition()
            if surrondingobjects.left == "N" and self.GetCurrentBlock() != "E":
                self.UpdateBlock("WA")

            escapeCounter = 0
            while surrondingobjects.forward not in ["0","E"]:
                self.turnright()
                surrondingobjects = self._getsurroundingobjects()
                escapeCounter += 1
                if escapeCounter > 100:
                    print("breaking out of infinite loop")
                    break



            
            counter = 0
            for i in surrondingobjects:
                if i =="WA":
                    counter += 1
            if counter == 2:
                self.UpdateBlock("WA")

            if surrondingobjects.forward == "0" and surrondingobjects.backward == "0" \
                    and self.furnitureonlevellimitreached() and self.GetCurrentBlock() != "E":
                temp = self._placefurniture()
                if temp is not None:
                    self.furniturepos.append([temp, Position(self.position.getx,self.position.getz), self.level])

                    

            # print(self.position)
            # print("Current Block: " + str(self.GetCurrentBlock()))
            # print("New Direction: " + str(self.direction))
            # self.printfloorplans()

            self.move()
            steps += 1
            if self.GetCurrentBlock() == "E" or steps > 99:
                # print("Back to start, steps taken: " + str(steps))
                if len(self.floorplans) > self.level+1:
                    self.setupnextlevel()
                    print("New level")
                    continue

                break
        self.FurniturePlacement()
        self.floorplans[0][self.savedblock[0][2]][self.savedblock[0][1]] = self.savedblock[0][0]

    def FurniturePlacement(self):
        for furniture in self.furniturepos:
            self.PlaceInMap(furniture[0],furniture[1],furniture[2])

    def furnitureonlevellimitreached(self):
        currentlevel = self.level
        nroffurniture = 0
        for furniture in self.furniturepos:
            if furniture[2] == currentlevel:
                nroffurniture +=1
        if nroffurniture >= self.furperlevel:
            return False
        else:
            return True

    def GetCurrentBlock(self):
        # if self.floorplans < 1:
        #     return self.floorplans[self.position.getz][self.position.getx]
        # else:
        return self.floorplans[self.level][self.position.getz][self.position.getx]

    def Position(self, xval, zval):
        self.position = Position(xval, zval)

    @property
    def position(self):
        return self.position

    def move(self):
        if self.direction == Direction.NORTH:
            self.position.subz()
        elif self.direction == Direction.EAST:
            self.position.addx()
        elif self.direction == Direction.SOUTH:
            self.position.addz()
        elif self.direction == Direction.WEST:
            self.position.subx()

    def peek(self, direction):
        pos = Position()
        if direction == Direction.NORTH:
            pos = Position(self.position.getx, self.position.getz - 1)
        elif direction == Direction.EAST:
            pos = Position(self.position.getx + 1, self.position.getz)
        elif direction == Direction.SOUTH:
            pos = Position(self.position.getx, self.position.getz + 1)
        elif direction == Direction.WEST:
            pos = Position(self.position.getx - 1, self.position.getz)
        return self.floorplans[self.level][pos.getz][pos.getx]

    def peekforward(self):
        peek = ""
        if self.direction == Direction.NORTH:
            peek = self.peek(Direction.NORTH)
        elif self.direction == Direction.EAST:
            peek = self.peek(Direction.EAST)
        elif self.direction == Direction.SOUTH:
            peek = self.peek(Direction.SOUTH)
        elif self.direction == Direction.WEST:
            peek = self.peek(Direction.WEST)
        return peek

    def getleftposition(self):
        pos = Position()
        if self.direction == Direction.NORTH:
            pos = Position(self.position.getx - 1, self.position.getz)
        elif self.direction == Direction.EAST:
            pos = Position(self.position.getx, self.position.getz - 1)
        elif self.direction == Direction.SOUTH:
            pos = Position(self.position.getx + 1, self.position.getz)
        elif self.direction == Direction.WEST:
            pos = Position(self.position.getx, self.position.getz + 1)
        return pos

    def peekright(self):
        peek = ""
        if self.direction == Direction.NORTH:
            peek = self.peek(Direction.EAST)
        elif self.direction == Direction.EAST:
            peek = self.peek(Direction.SOUTH)
        elif self.direction == Direction.SOUTH:
            peek = self.peek(Direction.WEST)
        elif self.direction == Direction.WEST:
            peek = self.peek(Direction.NORTH)
        return peek

    def peekleft(self):
        peek = ""
        if self.direction == Direction.NORTH:
            peek = self.peek(Direction.WEST)
        elif self.direction == Direction.EAST:
            peek = self.peek(Direction.NORTH)
        elif self.direction == Direction.SOUTH:
            peek = self.peek(Direction.EAST)
        elif self.direction == Direction.WEST:
            peek = self.peek(Direction.SOUTH)
        return peek
    def peekbackwards(self):
        peek = ""
        if self.direction == Direction.NORTH:
            peek = self.peek(Direction.SOUTH)
        elif self.direction == Direction.EAST:
            peek = self.peek(Direction.WEST)
        elif self.direction == Direction.SOUTH:
            peek = self.peek(Direction.NORTH)
        elif self.direction == Direction.WEST:
            peek = self.peek(Direction.EAST)
        return peek

    def PlaceInMap(self, string, position ,level):
        # type: (str, Position, int) -> None
        self.floorplans[level][position.getz][position.getx] = string


    def UpdateBlock(self, string):
        if string is not None:
            self.floorplans[self.level][self.position.getz][self.position.getx] = string

    def setup(self):
        zsize = len(self.floorplans[0])
        xsize = len(self.floorplans[0][0])

        self._setpostodoor(xsize, zsize)

        # determine starting direction.
        if self.position.getx == 0:
            self.direction = Direction.EAST
        elif self.position.getx == xsize - 1:
            self.direction = Direction.WEST
        elif self.position.getz == 0:
            self.direction = Direction.SOUTH
        elif self.position.getz == zsize - 1:
            self.direction = Direction.NORTH
        # first move
        self.move()
        self.savedblock.append([self.GetCurrentBlock(),self.position.getx,self.position.getz])
        self.UpdateBlock("E")

    def _setpostodoor(self, xsize, zsize):
        for z in range(zsize):
            for x in range(xsize):
                if self.floorplans[0][z][x] == "D":
                    self.Position(x, z)
                    return

    def turnleft(self):
        if self.direction == Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.EAST:
            self.direction = Direction.NORTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.WEST:
            self.direction = Direction.SOUTH

    def turnright(self):
        if self.direction == Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.NORTH

    def printfloorplans(self):
        list = []
        print("Floorplan:")

        for z in range(len(self.floorplans[self.level])):
            line = []
            for x in range(len(self.floorplans[self.level][z])):
                if z == self.position.getz and x == self.position.getx:
                    line.append("A")
                else:
                    line.append(self.floorplans[self.level][z][x])
            list.append(line)
        for i in list:
            print(i)
        # time.sleep(1)

    def getdirectionnextlevel(self, dirchar):
        if dirchar == "N":
            self.nextlevelstartingdirection = Direction.NORTH
        elif dirchar == "E":
            self.nextlevelstartingdirection = Direction.EAST
        elif dirchar == "S":
            self.nextlevelstartingdirection = Direction.SOUTH
        elif dirchar == "W":
            self.nextlevelstartingdirection = Direction.WEST

    def setupnextlevel(self):
        self.level += 1
        self.Position(self.nextlevelstartingpos.getx, self.nextlevelstartingpos.getz)
        self.direction = self.nextlevelstartingdirection

    def _getsurroundingobjects(self):
        return _Surrounding(self.peekforward(),self.peekright(),self.peekbackwards(),self.peekleft())

    def _getfurniture(self):

        levels = len(self.floorplans) / 2
        zsize = len(self.floorplans[0])
        xsize = len(self.floorplans[0][0])
        nroffurniture = int((levels * zsize * xsize) * .15)
        furnitures = []
        if nroffurniture <=1:
            nroffurniture = 4

        furnitures.append(["C", int(nroffurniture * .3)])
        furnitures.append(["F", int(nroffurniture * .3)])
        furnitures.append(["B", int(nroffurniture * .3)])
        furnitures.append(["S", int(nroffurniture * .3)])

        temp = 0
        for i in furnitures:
            temp +=i[1]

        self.furperlevel = int(temp/2)
        print(self.furperlevel)
        return furnitures

    def _placefurniture(self):
        random = rand.random()
        if len(self.furnitures) >0:
            if random < .5:
                furniture = rand.choice(self.furnitures)
                temp = furniture[0]
                if furniture[1] >0:
                    if temp != "S":
                        temp += self.getfurnituredir()
                    furniture[1] -=1
                    if furniture[1] == 0:
                        self.furnitures.remove(furniture)
                    return temp

    def getfurnituredir(self):
        char ="N"
        if self.direction == Direction.NORTH:
            char = "E"
        elif self.direction == Direction.EAST:
            char = "S"
        elif self.direction == Direction.SOUTH:
            char = "W"
        elif self.direction == Direction.WEST:
            char = "N"

        return char



def main():
    floorplan = \
        [
            [
                ['W', 'G', 'G', 'W', 'W', 'W'],
                ['W', '0', '0', '0', '0', 'G'],
                ['G', '0', '0', '0', '0', 'G'],
                ['G', '0', '0', '0', '0', 'G'],
                ['W', '0', '0', '0', 'E', 'D'],
                ['W', 'G', 'G', 'W', 'W', 'W']
            ],
        ]
    # floorplan = \
    #     [
    #         [
    #             ['W', 'W', 'W', 'G', 'G', 'W'],
    #             ['W', '0', '0', '0', '0', 'W'],
    #             ['G', '0', '0', '0', '0', 'W'],
    #             ['G', 'STN4', '0', '0', 'E', 'D'],
    #             ['G', 'STN3', '0', '0', '0', 'W'],
    #             ['G', 'STN2', '0', '0', '0', 'W'],
    #             ['G', 'CO2', 'STW1', 'STW0', '0', 'W'],
    #             ['W', 'G', 'G', 'G', 'G', 'W']
    #         ],
    #         [
    #             ['W', 'G', 'G', 'W', 'W', 'W'],
    #             ['G', '0', '0', '0', '0', 'W'],
    #             ['G', '0', '0', '0', '0', 'G'],
    #             ['G', 'E', '0', '0', '0', 'G'],
    #             ['G', 'N', '0', '0', '0', 'G'],
    #             ['G', 'N', '0', '0', '0', 'G'],
    #             ['W', 'N', 'N', '0', '0', 'W'],
    #             ['W', 'G', 'G', 'G', 'W', 'W']
    #         ]
    #     ]
    # floorplan = \
    #     [
    #         [
    #             ['W', 'G', 'G', 'G', 'G', 'G', 'G', 'W', 'W', 'W'],
    #             ['W', 'CO2', 'STE2', 'STE3', 'STE4', '0', '0', '0', '0', 'W'],
    #             ['G', 'STN1', '0', '0', '0', '0', '0', '0', '0', 'W'],
    #             ['G', 'STN0', '0', '0', '0', '0', '0', '0', '0', 'G'],
    #             ['G', '0', '0', '0', '0', '0', '0', '0', '0', 'G'],
    #             ['W', '0', '0', '0', '0', '0', '0', '0', 'E', 'D'],
    #             ['W', 'G', 'G', 'W', 'W', 'W', 'G', 'G', 'G', 'W']
    #         ],
    #         [
    #             ['W', 'G', 'G', 'W', 'G', 'G', 'W', 'W', 'W', 'W'],
    #             ['W', 'N', 'N', 'N', 'E', '0', '0', '0', '0', 'G'],
    #             ['G', 'N', '0', '0', '0', '0', '0', '0', '0', 'G'],
    #             ['G', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
    #             ['G', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
    #             ['G', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
    #             ['W', 'W', 'G', 'G', 'G', 'W', 'W', 'G', 'G', 'W']
    #         ]
    #     ]
    # floorplan = \
    #     [
    #         [
    #             ['W', 'G', 'G', 'G', 'W', 'W'],
    #             ['G', 'CO3', 'STW2', 'STW1', 'STW0', 'W'],
    #             ['G', 'STS3', '0', '0', '0', 'W'],
    #             ['G', 'STS4', '0', '0', '0', 'G'],
    #             ['W', '0', '0', '0', '0', 'G'],
    #             ['W', '0', '0', '0', '0', 'D'],
    #             ['W', '0', '0', '0', '0', 'W'],
    #             ['W', 'W', 'G', 'G', 'G', 'W'],
    #         ],
    #         [
    #             ['W', 'G', 'G', 'G', 'G', 'W'],
    #             ['G', 'N', 'N', 'N', '0', 'W'],
    #             ['G', 'N', '0', '0', '0', 'G'],
    #             ['G', 'E', '0', '0', '0', 'G'],
    #             ['G', '0', '0', '0', '0', 'W'],
    #             ['G', '0', '0', '0', '0', 'W'],
    #             ['W', '0', '0', '0', '0', 'W'],
    #             ['W', 'W', 'G', 'G', 'G', 'W']
    #         ]
    #     ]
    # floorplan = [[
    #     ['W', 'W', 'G', 'G', 'G', 'G', 'G', 'W'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'D'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', 'STN4', '0', '0', '0', '0', '0', 'G'],
    #     ['G', 'STN3', '0', '0', '0', '0', '0', 'G'],
    #     ['G', 'STN2', '0', '0', '0', '0', '0', 'G'],
    #     ['G', 'CO2', 'STW1', 'STW0', '0', '0', '0', 'W'],
    #     ['W', 'G', 'G', 'G', 'G', 'G', 'G', 'W'],
    # ],
    #     ['W', 'G', 'G', 'G', 'G', 'G', 'G', 'W'],
    #     ['W', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'G'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'G'],
    #     ['G', '0', '0', '0', '0', '0', '0', 'W'],
    #     ['G', 'E', '0', '0', '0', '0', '0', 'G'],
    #     ['G', 'N', '0', '0', '0', '0', '0', 'G'],
    #     ['G', 'N', '0', '0', '0', '0', '0', 'G'],
    #     ['G', 'N', 'N', 'N', '0', '0', '0', 'G'],
    #     ['W', 'W', 'W', 'W', 'G', 'G', 'G', 'W'],
    # ]
    # print(str(len(floorplan)))
    # print(floorplan)

    # agent.UpdateBlock("F")
    # print(agent.peek(Direction.NORTH))
    # print(agent.GetCurrentBlock())
    # print(agent.position)
    # print(agent.direction)
    agent = FurnitureAgent(floorplan)
    agent.Act()


if __name__ == "__main__":
    main()


