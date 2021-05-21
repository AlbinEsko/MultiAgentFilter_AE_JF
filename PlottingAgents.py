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

class PlotAgent:
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 1
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.blockPos = Vector(0,0)
        self.dir = Vector(1,0)
        self.dir.rotate_ip(Random.randint(0,359))
        
    def Act(self):
        if not self.Move():
            #print("same tile")
            return
        #print("new tile", int(self.pos.x), int(self.pos.y))
        self.Evaluate()

    '''Wander around 
    Keep close to existing roads'''
    def Move(self):
        oldPos = self.pos
        if(not self.OutOfBounds()):
            self.pos += self.dir * self.speed
            self.dir.rotate_ip(Random.randint(-20,20)) #Needs improvement for the wanted wandering behavior; move to roadMap values of zero
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
        blockPos = Vector(int(p.x),int(p.y))
        return blockPos
    
    def TraceTraveledPath(self):
        uf.setBlock(self.roadSystem.level, (35,0), int(self.roadSystem.origo.x + self.pos.x), self.roadSystem.heightMap[int(self.pos.y)][int(self.pos.x)], int(self.roadSystem.origo.y + self.pos.y ))
    
    def Evaluate(self):
        posIndex = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        currentNode = self.roadSystem.graph[posIndex]
        if currentNode.roadVal == 99 and currentNode.plotted == True:
            return
        roadConnection = self.FindClosestRoad(currentNode)
        evaluatedPlot = Plot(roadConnection.height, Vector(roadConnection.x, roadConnection.y))
        self.FillPlot(evaluatedPlot)
    
    '''Analyze current position for suitable plot'''
    def Analyze(self, currentNode):
        self.FindClosestRoad(currentNode)
        return
        
    def FindClosestRoad(self, currentNode):
        node = currentNode
        while node.roadVal < self.roadSystem.roadCoverage:
             node = self.CheckSurroundingTiles(node)
             
        return node
    
    def CheckSurroundingTiles(self, node):
        largestRoadVal = 0
        for x in (-1, 0, 1): #print top row of current layer
            for y in (-1, 0, 1):
                if x == 0 and y == 0:
                    continue
                nextNode = self.roadSystem.graph.getNode(node.x + x, node.y + y)
                if nextNode.roadVal > largestRoadVal:
                    largestRoadVal = nextNode.roadVal
                    closestNode = nextNode
        return closestNode
    
    def FillPlot(self, plot):
        return
    
    
class Plot:
    def __init__(self, bottomLevel, entranceCoords):
        self.bottomLevel = bottomLevel
        self.entranceCoords = entranceCoords
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    