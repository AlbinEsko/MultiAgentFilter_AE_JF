# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:50:43 2021

@author: golf_
"""

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

import utilityFunctions as uf

inputs = (
	("First Test", "label"),
    ("Material", alphaMaterials.Cobblestone), 
	("Creator: Albin Esko", "label"),
	)
'''
def perform(level,box,options):
    block = (level.blockAt(box.minx,box.miny,box.minz), level.blockDataAt(box.minx, box.miny, box.minz))
    print(block)
'''
'''
def perform(level, box, options):
    print("finding heightmap")
    heightmap = []
    for x in range(box.minx, box.maxx, 1):
        for z in range(box.minz, box.maxz, 1):
            for y in range(box.maxy-1, box.miny-1, -1):
                if(level.blockAt(x,y,z) != 0):
                    heightmap.append(y)
                    uf.setBlock(level,(options["Material"].ID, options["Material"].blockData),x,y,z)
                    break
    index = 0
    for height in heightmap:
        print(index)
        x = index / uf.getBoxSize(box)[2]
        z = index % uf.getBoxSize(box)[2]
        print("X:{0}, Z:{1}, Height: {2}".format(x,z,height))
        index = index + 1

'''
def perform(level, box, options):
    print(alphaMaterials.Cobblestone)
    print(alphaMaterials[4,0])
    print(alphaMaterials.type)
    print(type(alphaMaterials))

