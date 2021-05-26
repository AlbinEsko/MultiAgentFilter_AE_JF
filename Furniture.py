import utilityFunctions as uf
import random as random
from MAF_Utility import Direction



class Bookshelf:
    def __init__(self, level, x,y,z, r = random.random()):
        # print("Building Bookshelf")
        block = 47
        data = 0
        uf.setBlock(level,(block,data), x,y,z)
        uf.setBlock(level,(block,data), x,y+1,z)
        r = random.random()
        if r >0.5:
            uf.setBlock(level, (block, data), x, y + 2, z)


class Stair:
    def __init__(self,level,x,y,z,direction, height=0, block=53):
        # print("Building Stair")
        data = 0
        if direction == 1:
            data = 3
        elif direction == 2:
            data = 0
        elif direction == 3:
            data = 2
        elif direction == 4:
            data = 1
        uf.setBlock(level,(block,data),x,y+height,z)
        if height >= 1:
            for i in range(3):
                uf.setBlock(level,(0,0),x,y+height+i+1,z)
        if height >0 and height < 3:
            r = random.random()
            spice = 5
            if r < 0.5:
                spice = 47
            for i in range(height):
                uf.setBlock(level, (spice, 0), x, y + height-1-i, z)


class Corner:
    def __init__(self,level,x,y,z, height, block=5, data=0):
        # print("Building Corner")
        for i in range(int(height)):
            uf.setBlock(level, (block, data), x, y+i, z)
        for i in range(3):
            uf.setBlock(level, (0, 0), x, y + int(height) + i, z)


class Bed:
    def __init__(self,level,x,y,z, direction):
        block = 26
        data1=0
        data2=0
        xoffset =0
        zoffset =0
        if direction == 1:  # NORTH
            data1 = 10
            data2 = 2
            zoffset = +1
        elif direction == 2:  # EAST
            data1 = 11
            data2 = 3
            xoffset = -1
        elif direction == 3:  # SOUTH
            data1 = 8
            data2 = 0
            zoffset = -1
        elif direction == 4:  # WEST
            data1 = 9
            data2 = 1
            xoffset = 1
        uf.setBlock(level,(block,data1),x,y,z)
        uf.setBlock(level,(block,data2),x+xoffset,y,z+zoffset)

class Furnace:
    def __init__(self, level, x, y, z, direction):
        # print("Building Furnace")
        block = 61
        data = 0
        if direction == 1:  # NORTH
            data = 2
        elif direction == 2:  # EAST
            data = 5
        elif direction == 3:  # SOUTH
            data = 3
        elif direction == 4:  # WEST
            data = 4
        uf.setBlock(level, (block, data), x, y, z)

class Chest:
    def __init__(self,level, x, y, z, direction):
        # print("Building Chest")
        block = 54
        data = 0
        if direction == 1:  # NORTH
            data = 2
        elif direction == 2:  # EAST
            data = 5
        elif direction == 3:  # SOUTH
            data = 3
        elif direction == 4:  # WEST
            data = 4
        uf.setBlock(level, (block, data), x, y, z)