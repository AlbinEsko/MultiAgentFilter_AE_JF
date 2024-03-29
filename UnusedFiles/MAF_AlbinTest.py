# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:08:34 2021

@author: Albin Esko & Johan Fritiofsson
"""
from array import *
from pymclevel import alphaMaterials
import utilityFunctions as uf
import Graph as Graph
import BlockIDs as Blocks
from typing import List, Any
import Road as Road
from pygame.math import Vector2 as Vector
from MAF_Utility import Direction
from Building import House

inputs = (
    ("test1", "label"),
)


def perform(level, box, options):
    print("Performing")
    hgtMap, liquidmap = createHeightMap(level, box)
    print("height map and liquid map made")
    #markRegions(level, box, hgtMap, liquidmap)
    boxOrigo = Vector(box.minx, box.minz)
    print("Creating road graph")
    roads = Road.RoadSystem(level,box,hgtMap,liquidmap, boxOrigo)
    print("creating agents")
    roads.CreateExtendors(35)
    roads.CreateConnectors(50)
    itterations =box.length/2 + box.width/2
    print("Running road agents")
    for r in range(itterations):
        print("Road Creation: " + str(r) + "/" + str(itterations))
        roads.UpdateAgents()
    roads.CleanObstructions()
    roads.CreatePloters(5)
    print("Running Plot agents")
    for r in range(itterations):
        print("Plot Creation: " + str(r) + "/" + str(itterations))
        roads.UpdatePlotAgents()
    
    #roads.PrintPlots()
    for p in roads.plots:
        house = House(box, p.houseBounds, level, p.bottomLevel, Direction(p.doorDir))
        house.generate()


def createHeightMap(level, box):
    row = box.maxx - box.minx #vågräta
    column = box.maxz - box.minz #lodräta
    heightmap = [[0 for i in range(row)] for j in range(column)]
    liquidmap = [[0 for i in range(row)] for j in range(column)]

    #for r in heightmap:
        #print(r)

    for z in range(column):  # range(box.minx, box.maxx, 1):
        print("Columns scanned: " + str(z) + "/" + str(column))
        for x in range(row):  # range(box.minz, box.maxz, 1):
            for y in range(box.maxy, box.miny, -1):
                block = level.blockAt(box.minx+x, y, box.minz+z) 
                if block == 0:
                    continue
                if block in Blocks.getGrounds():
                    heightmap[z][x] = y
                    blockabove = level.blockAt(box.minx+x, y+1, box.minz+z)
                    if blockabove in Blocks.getLiquids():
                        if blockabove in [8, 9, 79]:
                            liquidmap[z][x] = 1
                        else:
                            liquidmap[z][x] = 2                   

                    break

    #for r in liquidmap:
    #    print(r)

    return heightmap, liquidmap

def printRegions(level, box, regions):
    blocktype=35
    blockid=0
    for r in regions:
        blockid = (blockid+1) % 16
        for b in r:
            uf.setBlock(level,(blocktype,blockid),box.minx+b[0],100,box.minz+b[1])

def markRegions(level, box, hgtMap, liquidmap):
    regions=Graph.connectivity(hgtMap)
    #regions= Graph.liquidMap(liquidmap)
    #print(regions[0])
    blocktype=35
    blockid=0
    for r in regions:
        blockid = (blockid+1) % 16
        for b in r:
            uf.setBlock(level,(blocktype,blockid),box.minx+b[0],100,box.minz+b[1])
