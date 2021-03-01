
from pymclevel import mclevel


def GetBlockType(level, x, y, z):
    return level.blockAt(x, y, z), level.blockDataAt(x,y,z)
def GetBlockName(level, x,y,z):
    return level.materials[level.blockAt(x, y, z), level.blockDataAt(x,y,z)]