# -*- coding: utf-8 -*-
"""
Created on Fri May 21 13:15:26 2021

@author: Albin Esko
"""

import sys
import heapq
import numpy as np
import random as Random
from pygame.math import Vector2 as Vector
import Graph as Graph
import Dijkstra
import utilityFunctions as uf
import Road
import Queue as q
from pymclevel import box
import BlockIDs as Blocks

class PlotAgent:
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 4
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.blockPos = Vector(0,0)
        self.dir = Vector(1,0)
        self.dir.rotate_ip(Random.randint(0,359))
        
    def Act(self):
        if not self.Move():
            return
        self.Evaluate()

    '''Wander around 
    Keep close to existing roads'''
    def Move(self):
        oldPos = self.pos
        if(not self.OutOfBounds()):
            self.pos += self.dir * self.speed
            self.dir.rotate_ip(Random.randint(-20,20))
        else:
            self.dir.rotate_ip(180)
            self.pos += self.dir * self.speed
        return self.ConvertToIntCoords(self.pos) == self.ConvertToIntCoords(oldPos)
    
    def OutOfBounds(self):
        if(self.pos.x + self.dir.x * self.speed < 0):
            return True
        if(self.pos.y + self.dir.y * self.speed < 0):
            return True
        if(self.pos.x + self.dir.x * self.speed >= self.roadSystem.width):
            return True
        if(self.pos.y + self.dir.y * self.speed >= self.roadSystem.height):
            return True
        return False
    
    def ConvertToIntCoords(self, p):
        return Vector(int(p.x),int(p.y))
    
    def TraceTraveledPath(self):
        uf.setBlock(self.roadSystem.level, (35,10), int(self.roadSystem.origo.x + self.pos.x), self.roadSystem.heightMap[int(self.pos.y)][int(self.pos.x)], int(self.roadSystem.origo.y + self.pos.y ))
    
    def Evaluate(self):
        posIndex = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        currentNode = self.roadSystem.graph[posIndex]
        if currentNode.roadVal == 0:
            self.dir.rotate_ip(Random.randint(160,200))
            return False
        if currentNode.roadVal >= self.roadSystem.roadCoverage or currentNode.plotted == True:
            #print("On road or other plot or too far")
            return False
        roadConnection = self.FindClosestRoad(currentNode)
        #print("creating plot")
        evaluatedPlot = Plot(roadConnection.height, Vector(roadConnection.x, roadConnection.y), self.roadSystem.origo)
        #print("expanding plot")
        
        #print("evaluate plot")
        if evaluatedPlot.FillPlot(self.roadSystem.graph, self.roadSystem.roadCoverage - 1, self.roadSystem.level):
            self.roadSystem.plots.append(evaluatedPlot)
            #print("plot created", evaluatedPlot.houseBounds.width, evaluatedPlot.houseBounds.length)
            return True
        else:
            #print("plot regected", len(evaluatedPlot.tiles))
            evaluatedPlot.SelfDestruct()
            return False

        
    def FindClosestRoad(self, currentNode):
        node = currentNode
        while node.roadVal < self.roadSystem.roadCoverage-1:
             node = self.CheckSurroundingTiles(node)
        return node
    
    def CheckSurroundingTiles(self, node):
        largestRoadVal = 0
        closestNode = node
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == 0 and y == 0:
                    continue
                if node.x + x >= 0 and node.x + x < self.roadSystem.width and node.y + y >= 0 and node.y + y < self.roadSystem.height:
                    nextNode = self.roadSystem.graph.getNode(node.x + x, node.y + y)
                    if nextNode.roadVal > largestRoadVal:
                        largestRoadVal = nextNode.roadVal
                        closestNode = nextNode

        return closestNode
    
    
class Plot:
    def __init__(self, bottomLevel, entranceCoords, worldOffset):
        self.bottomLevel = bottomLevel
        self.entranceCoords = entranceCoords
        self.tiles = []
        self.maxSide = 12
        #self.boundingWidth
        #self.boundingHeight
        #self.offsetX
        #self.offsetY
        self.houseTiles = []
        self.worldOffset = worldOffset
        self.doorDir = 0
        
    def AddTile(self, tile):
        self.tiles.append(tile)
        tile.plotted = True
    
    def FinalizePlot(self, entrance, level):
        self.tiles.remove(entrance)
        self.tiles.sort()
        self.FindMaxBoundings()
        self.PlaceTilesInMaxBound()
        if self.FindHouseBounds():
            self.ModifyTerrain(level)
            return True
        return False
    
    def PrintPlot(self, level, origo, data):
        origoX = int(origo.x)
        origoY = int(origo.y)
        for t in self.tiles:
            uf.setBlock(level, (35,data), origoX + t.x, self.bottomLevel, origoY + t.y)
        uf.setBlock(level, (35,data), origoX + int(self.entranceCoords.x), self.bottomLevel + 1, origoY + int(self.entranceCoords.y))
        #for t in self.houseTiles:
            #uf.setBlock(level, (35,data), origoX + t.x, self.bottomLevel + 1, origoY + t.y)
        #print(self.houseBounds)
        for y in range(self.houseBounds.length):
            for x in range(self.houseBounds.width):
                uf.setBlock(level, (35,data), self.houseBounds.minx + x, self.bottomLevel + 1, self.houseBounds.minz + y)
        
    def SelfDestruct(self):
        for t in self.tiles:
            t.plotted = False
            
    def FindMaxBoundings(self):
        minX = sys.maxint
        maxX = -1
        minY = sys.maxint
        maxY = -1
        for t in self.tiles:
            minX = min(minX, t.x)
            maxX = max(maxX, t.x)
            minY = min(minY, t.y)
            maxY = max(maxY, t.y)
        self.boundingWidth = maxX - minX + 1
        self.boundingHeight = maxY - minY + 1
        self.offsetX = minX
        self.offsetY = minY
        
    def PlaceTilesInMaxBound(self):
        #print("Width, height", self.boundingWidth, self.boundingHeight)
        self.maxBoundingBox = [[None for i in range(self.boundingWidth)] for j in range(self.boundingHeight)]
        for t in self.tiles:
            #print("x, y:",t.x-self.offsetX, t.y-self.offsetY)
            self.maxBoundingBox[t.y-self.offsetY][t.x-self.offsetX] = t
        
    def FindHouseBounds(self):
        largestPlot = (0,0,0,0)
        for t in self.tiles:
            x0 = t.x - self.offsetX
            y0 = t.y - self.offsetY
            width = 1
            height = 1
            expanded = True
            while expanded:
                expanded = False
                if x0 + (width-1) + 1 < self.boundingWidth:
                    valid=True
                    for i in range(height):
                        if self.maxBoundingBox[y0+i][x0 + width-1 + 1] == None:
                            valid = False
                            break
                    if valid:
                        width += 1
                        expanded = True
                if y0 + (height-1) + 1 < self.boundingHeight:
                    valid=True
                    for i in range(width):
                        if self.maxBoundingBox[y0 + height-1 + 1][x0 + i] == None:
                            valid = False
                            break
                    if valid:
                        height += 1
                        expanded = True
            if width * height > largestPlot[2] * largestPlot[3]:
                largestPlot = (x0, y0, width, height)
                #print("largest plot set:",largestPlot)
            
        for y in range(largestPlot[3]):
            for x in range(largestPlot[2]):
                self.houseTiles.append(self.maxBoundingBox[largestPlot[1]+y][largestPlot[0]+x])
        
        self.houseBounds = box.BoundingBox((largestPlot[0] + self.offsetX + int(self.worldOffset.x), 0, largestPlot[1] + self.offsetY + int(self.worldOffset.y) + 1),(largestPlot[2]-2, 1, largestPlot[3]))
        if self.houseBounds.width < 6 or self.houseBounds.length < 6:
            #print("too small", self.houseBounds.width, self.houseBounds.length)
            return False
        
        boxXcentre = self.houseBounds.minx + self.houseBounds.width/2
        boxYcentre = self.houseBounds.minz + self.houseBounds.length/2
        centToEntX = int(self.entranceCoords.x) - boxXcentre
        centToEntY = int(self.entranceCoords.y) - boxYcentre
        if abs(centToEntX) > abs(centToEntY):
            if centToEntX < 0:
                self.doorDir = 4
            else:
                self.doorDir = 2
        else:
            if centToEntY < 0:
                self.doorDir = 1
            else:
                self.doorDir = 3
                
        print("housable plot found", self.houseBounds.width, self.houseBounds.length)
        return True
    
    def FillPlot(self, graph, stopRoadVal, level):
        start = self.entranceCoords
        startNode = graph.getNode(int(start.x), int(start.y))
        maxX = startNode.x
        minX = startNode.x
        maxY = startNode.y
        minY = startNode.y
        enqueued = [False for i in range(graph.nrNodes)]
        stack = []
        stack.append(startNode)
        enqueued[startNode.index] = True
        while(len(stack) > 0):
            #print(len(stack))
            activeNode = stack.pop()
            self.AddTile(activeNode)
            for e in activeNode.adjacent:
                toNode = graph[e.to]
                if toNode.x - activeNode.x != 0 and toNode.y - activeNode.y != 0: #to prevent diagonal traversal
                    continue
                if enqueued[toNode.index] or toNode.plotted or toNode.roadVal >= stopRoadVal:
                    enqueued[toNode.index] = True
                    continue
                enqueued[toNode.index] = True
                toX = toNode.x
                toY = toNode.y
                
                if toX <= maxX and toX >= minX and toY <= maxY and toY >= minY: #check if inside already established bounds
                    stack.append(toNode)
                    #print("inside bounds")
                    continue
                if maxX - minX >= self.maxSide and maxY - minY >= self.maxSide:
                    continue
                
                #check if expansion of bounds is allowed
                expanded = False
                if toX < minX and maxX - toX < self.maxSide:
                    minX = toX
                    expanded = True
                if toX > maxX and toX - minX < self.maxSide:
                    maxX = toX
                    expanded = True
                if toY < minY and maxY - toY < self.maxSide:
                    minY = toY
                    expanded = True
                if toY > maxY and toY - minY < self.maxSide:
                    maxY = toY
                    expanded = True
                if expanded:
                    stack.append(toNode)
                    #print("expanded bounds")
        return self.FinalizePlot(startNode, level)
    
    def ModifyTerrain(self, level):
        airBelow = True
        y = self.bottomLevel
        while airBelow:
            airBelow = False
            for z in range(self.houseBounds.length):
                for x in range(self.houseBounds.width):
                    block = level.blockAt(self.houseBounds.minx + x, y, self.houseBounds.minz + z) 
                    if not block in Blocks.getGrounds():
                        uf.setBlock(level, (98,0), self.houseBounds.minx + x, y, self.houseBounds.minz + z)
                        airBelow = True
            y += -1
        
        blocksAbove = True
        y = self.bottomLevel
        while blocksAbove:
            blocksAbove = False
            y += 1
            for z in range(self.houseBounds.length):
                for x in range(self.houseBounds.width):
                    if level.blockAt(self.houseBounds.minx + x,y,self.houseBounds.minz + z) != 0:
                        uf.setBlock(level, (0,0), self.houseBounds.minx + x, y, self.houseBounds.minz + z)
                        blocksAbove = True
                

    
    
    