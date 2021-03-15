# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:08:34 2021

@author: Albin Esko & Johan Fritiofsson
"""
from array import *
from pymclevel import alphaMaterials
import utilityFunctions as uf
import Graph as Graph
from typing import List, Any

inputs = (
    ("test1", "label"),
)


def perform(level, box, options):
    print("Armed and ready")
    hgtMap = createHeightMap(level, box)
    markRegions(level, box, hgtMap)
    

def createHeightMap(level, box):
    row = box.maxx - box.minx #vågräta
    column = box.maxz - box.minz #lodräta
    heightmap = [[0 for i in range(row)] for j in range(column)]

    for r in heightmap:
        print(r)

    for z in range(column):  # range(box.minx, box.maxx, 1):
        for x in range(row):  # range(box.minz, box.maxz, 1):
            for y in range(box.maxy, box.miny, -1):
                if (level.blockAt(box.minx+x, y, box.minz+z)) != 0:
                    heightmap[z][x] = y

                    break

    for r in heightmap:
        print(r)

    return heightmap

def markRegions(level, box, hgtMap):
    regions=Graph.connectivity(hgtMap)
    print(regions[0])
    blocktype=0
    for r in regions:
        blocktype = blocktype+1
        for b in r:
            uf.setBlock(level,(blocktype,0),box.minx+b[0],100,box.minz+b[1])
