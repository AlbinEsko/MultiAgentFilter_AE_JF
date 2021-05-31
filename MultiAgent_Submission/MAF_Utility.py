from collections import namedtuple

from enum import Enum
# from pymclevel import mclevel
#
#
# def GetBlockType(level, x, y, z):
#     return level.blockAt(x, y, z), level.blockDataAt(x, y, z)
#
#
# def GetBlockName(level, x, y, z):
#     return level.materials[level.blockAt(x, y, z), level.blockDataAt(x, y, z)]
#

class Direction(Enum):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4



