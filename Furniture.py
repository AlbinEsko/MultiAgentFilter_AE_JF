import utilityFunctions as uf
import random as random



class Bookshelf:
    def __init__(self, level, x,y,z, direction=None):
        print("Building Bookshelf")
        block = 47
        data = 0
        uf.setBlock(level,(block,data), x,y,z)
        uf.setBlock(level,(block,data), x,y+1,z)
        r = random.random()
        if r <0.5:
            uf.setBlock(level, (block, data), x, y + 2, z)