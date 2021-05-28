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

class PlotAgent:
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 4
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.blockPos = Vector(0,0)
        self.dir = Vector(1,0)
        self.dir.rotate_ip(Random.randint(0,359))
        #self.plotted = False
        
    def Act(self):
        #if self.plotted:
            #return
        if not self.Move():
            return
        #self.TraceTraveledPath()
        self.Evaluate()
        #self.plotted = True

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
        return Vector(int(p.x),int(p.y))
    
    def TraceTraveledPath(self):
        uf.setBlock(self.roadSystem.level, (35,10), int(self.roadSystem.origo.x + self.pos.x), self.roadSystem.heightMap[int(self.pos.y)][int(self.pos.x)], int(self.roadSystem.origo.y + self.pos.y ))
    
    def Evaluate(self):
        posIndex = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        currentNode = self.roadSystem.graph[posIndex]
        if currentNode.roadVal >= self.roadSystem.roadCoverage or currentNode.plotted == True or currentNode.roadVal == 0:
            print("On road or other plot or too far")
            return
        roadConnection = self.FindClosestRoad(currentNode)#risk of infinite loop when a tile is surrounded by only 0s as road value
        #print("creating plot")
        evaluatedPlot = Plot(roadConnection.height, Vector(roadConnection.x, roadConnection.y))
        #print("expanding plot")
        evaluatedPlot = self.FillPlot(evaluatedPlot)
        #print("evaluate plot")
        if len(evaluatedPlot.tiles) > 9:
            self.roadSystem.plots.append(evaluatedPlot)
            print("plot created")
        else:
            print("plot regected", len(evaluatedPlot.tiles))
            evaluatedPlot.SelfDestruct()

        
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
    
    def FillPlot(self, plot):
        graph = self.roadSystem.graph
        start = plot.entranceCoords
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
            plot.AddTile(activeNode)
            for e in activeNode.adjacent:
                toNode = graph[e.to]
                if toNode.x - activeNode.x != 0 and toNode.y - activeNode.y != 0: #to prevent diagonal traversal
                    continue
                if enqueued[toNode.index] or toNode.plotted or toNode.roadVal >= self.roadSystem.roadCoverage-1:
                    enqueued[toNode.index] = True
                    continue
                enqueued[toNode.index] = True
                toX = toNode.x
                toY = toNode.y
                
                if toX <= maxX and toX >= minX and toY <= maxY and toY >= minY: #check if inside already established bounds
                    stack.append(toNode)
                    #print("inside bounds")
                    continue
                if maxX - minX >= plot.maxSide and maxY - minY >= plot.maxSide:
                    continue
                
                #check if expansion of bounds is allowed
                expanded = False
                if toX < minX and maxX - toX < plot.maxSide:
                    minX = toX
                    expanded = True
                if toX > maxX and toX - minX < plot.maxSide:
                    maxX = toX
                    expanded = True
                if toY < minY and maxY - toY < plot.maxSide:
                    minY = toY
                    expanded = True
                if toY > maxY and toY - minY < plot.maxSide:
                    maxY = toY
                    expanded = True
                if expanded:
                    stack.append(toNode)
                    #print("expanded bounds")
        plot.RemoveEntrance(startNode)
        return plot
    
    
class Plot:
    def __init__(self, bottomLevel, entranceCoords):
        self.bottomLevel = bottomLevel
        self.entranceCoords = entranceCoords
        self.tiles = []
        self.maxSide = 10
        
    def AddTile(self, tile):
        self.tiles.append(tile)
        tile.plotted = True
    
    def RemoveEntrance(self, entrance):
        self.tiles.remove(entrance)
    
    def PrintPlot(self, level, origo, data):
        origoX = int(origo.x)
        origoY = int(origo.y)
        for t in self.tiles:
            uf.setBlock(level, (35,data), origoX + t.x, self.bottomLevel, origoY + t.y)
        uf.setBlock(level, (35,data), origoX + int(self.entranceCoords.x), self.bottomLevel + 1, origoY + int(self.entranceCoords.y))
        
    def SelfDestruct(self):
        for t in self.tiles:
            t.plotted = False
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    