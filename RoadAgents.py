# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:17:04 2021

@author: golf_
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

class ExtendorAgent:
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 1
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.blockPos = Vector(0,0)
        self.dir = Vector(1,0)
        self.dir.rotate_ip(Random.randint(0,359))
        
    def Act(self):
        if not self.Move():
            print("same tile")
            return
        #print("new tile", int(self.pos.x), int(self.pos.y))
        self.Analyze()

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
    
    '''Analyze current position for road coverage'''
    def Analyze(self):
        if self.roadSystem.graph.getNode(int(self.pos.x),int(self.pos.y)).roadVal == 0:
            #print("found unserviced patch")
            self.dijkstra()
            
    '''follow roadmap distance to existing road and log every step'''
    def MakeRoadWithDistance(self):
        path = []
        path.append([int(self.pos.x), (int(self.pos.y))])
        z=0
        while True:
            print(z)
            z = z+1
            X = path[len(path)-1][0]
            Y = path[len(path)-1][1]
            if self.roadSystem.roadMap[Y][X] == 99:
                break
            value=0
            nextX = -1
            nextY = -1
            topFree = Y-1 >= 0
            leftFree = X-1 >= 0
            botFree = Y+1 < self.roadSystem.height
            rightFree = X+1 < self.roadSystem.width
            if leftFree:
                if self.roadSystem.roadMap[Y][X-1] > value:
                    value, nextX, nextY = self.CheckValue(X-1,Y,value)
            if topFree:
                if self.roadSystem.roadMap[Y-1][X] > value:
                    value, nextX, nextY = self.CheckValue(X,Y-1,value)
            if rightFree:
                if self.roadSystem.roadMap[Y][X+1] > value:
                    value, nextX, nextY = self.CheckValue(X+1,Y,value)
            if botFree:
                if self.roadSystem.roadMap[Y+1][X] > value:
                    value, nextX, nextY = self.CheckValue(X,Y+1,value)
            if leftFree and topFree:
                if self.roadSystem.roadMap[Y-1][X-1] > value:
                    value, nextX, nextY = self.CheckValue(X-1,Y-1,value)
            if topFree and rightFree:
                if self.roadSystem.roadMap[Y-1][X+1] > value:
                    value, nextX, nextY = self.CheckValue(X+1,Y-1,value)
            if botFree and rightFree:
                if self.roadSystem.roadMap[Y+1][X+1] > value:
                    value, nextX, nextY = self.CheckValue(X+1,Y+1,value)
            if botFree and leftFree:
                if self.roadSystem.roadMap[Y+1][X-1] > value:
                    value, nextX, nextY = self.CheckValue(X-1,Y+1,value)
            #print(value, nextX, nextY)
            path.append([nextX, nextY])
            self.printRoad(path)
            
    def printRoad(self, path):
        while len(path) != 0:
            pos = path.roadTiles.pop()
            placeX = pos[0]
            placeY = pos[1]
            self.roadSystem.SetRoadMapTile(placeX, placeY)
            
    def printRoad_Ind(self, path):
        while len(path) != 0:
            pos = path.pop()
            placeX = pos % self.roadSystem.width
            placeY = pos / self.roadSystem.width
            self.roadSystem.SetRoadMapTile(placeX, placeY)
        
        
    def CheckValue(self, X, Y, value):
        value = self.roadSystem.roadMap[Y][X]
        nextX = X
        nextY = Y
        return value, nextX, nextY 

    def dijkstra(self):
        #creatiing full arrays for the whole area feels wastefull, further research for later
        start = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        if start >= self.roadSystem.graph.nrNodes:
            raise Exception("agent out of bounds at ", start, self.pos, int(self.pos.x), int(self.pos.y), self.roadSystem.width)
        d = Dijkstra.dijkstras(self.roadSystem.graph, start)
        to = d.buildToRoadMinSpanTree(self.roadSystem.graph)
        if to == -1:
            #print ("road construction aborted")
            return
        data = d.pathTo(to)
        path = Road.Path(data, self.roadSystem.width)
        if path.isEmpty():
            return
        self.pos = path.getLastCoord()
        self.dir.rotate_ip(Random.randint(0,359))
        #print("sending suggestion to roadsystem")
        self.roadSystem.Analyze(path, 1)
        
#########################################################
#########################################################
#########################################################
#########################################################
class ConnectorAgent:
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.oldPos = self.pos
        self.range = 64
        self.distanceMultiplier = 3.5 #Larger number leads to less roads
        self.minExistingDistForConnection = 30
    
    def Act(self):
        self.Move()
        self.SampleNearRoad()
    
    def Move(self):
        possibleMoves = self.ScanForAdacentroad()
        if len(possibleMoves) == 0:
            swap = self.pos
            self.pos = self.oldPos
            self.oldPos = swap
            #print("Doublebacked")
            return
        self.oldPos = self.pos
        self.pos = Random.choice(possibleMoves)
        #print(self.pos)
    
    def OutOfBounds(self, testDir):
        if(self.pos.x + testDir.x < 0):
            return True
        if(self.pos.y + testDir.y < 0):
            return True
        if(self.pos.x + testDir.x >= self.roadSystem.width):
            return True
        if(self.pos.y + testDir.y >= self.roadSystem.height):
            return True
        return False
    
    def ScanForAdacentroad(self):
        adjNodes = []
        look = Vector(1,0)
        for i in range(8):
            tempDir = look.rotate(i * 45)
            tempDir.x = round(tempDir.x)
            tempDir.y = round(tempDir.y)
            #temp dir is now of only integers
            if self.OutOfBounds(tempDir):
                continue
            if self.oldPos.distance_squared_to(self.pos + tempDir) < 0.1:
                continue
            nextNode = self.roadSystem.graph.getNode(int(self.pos.x + tempDir.x),int(self.pos.y + tempDir.y))
            if nextNode.roadVal == 99:
                adjNodes.append(self.pos + tempDir)
        return adjNodes
    
    def SampleNearRoad(self):
        posIndex = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        direction = Vector(1,0)
        direction.rotate_ip(Random.randint(0,359))
        endPoint = self.pos + direction * self.range
        #Digital differential analyzer algorithm
        dx = endPoint.x - self.pos.x
        dy = endPoint.y - self.pos.y
        step = max(abs(dx), abs(dy))
        dx /= step
        dy /= step
        x = self.pos.x
        y = self.pos.y
        i = 1
        while i <= step and x >= 0 and x < self.roadSystem.width-1 and y >= 0 and y < self.roadSystem.height-1:
            checkedNode = self.roadSystem.graph.getNode(int(x), int(y))
            if checkedNode.roadVal == 99 and checkedNode.index != posIndex:
                self.FindDistanceOnRoad(checkedNode)
                break
            x += dx
            y += dy
            i += 1
            
    def TraceTraveledPath(self):
        uf.setBlock(self.roadSystem.level, (35,0), int(self.roadSystem.origo.x + self.pos.x), self.roadSystem.heightMap[int(self.pos.y)][int(self.pos.x)], int(self.roadSystem.origo.y + self.pos.y ))
    
    def FindDistanceOnRoad(self,checkedNode):
        posIndex = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        #print(self.roadSystem.graph[posIndex].roadAdjacent)
        d = Dijkstra.dijkstras(self.roadSystem.graph, checkedNode.index)
        d.buildOnRoadMinSpanTree(self.roadSystem.graph)
        edges = d.pathTo(posIndex)
        if edges == None:
            print("no path found")
            return
        path = Road.Path(edges, self.roadSystem.width)
        eqldDist = np.sqrt(abs(int(self.pos.x) - checkedNode.x) ** 2 + abs(int(self.pos.y) - checkedNode.y) ** 2)
        #print(eqldDist)
        if path.totalWeight < max(self.minExistingDistForConnection, eqldDist * self.distanceMultiplier):
            #print("existing path close enough")
            return
        d = Dijkstra.dijkstras(self.roadSystem.graph, posIndex)
        d.buildCompleteMinSpanTree(self.roadSystem.graph)
        edges = d.pathTo(checkedNode.index)
        path = Road.Path(edges, self.roadSystem.width)
        print("Suggesting connection")
        if self.roadSystem.Analyze(path, 2):
            self.pos = path.getLastCoord()
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    