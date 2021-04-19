# -*- coding: utf-8 -*-
import numpy as np
import random as Random
from pygame.math import Vector2 as Vector
import Graph as Graph
import utilityFunctions as uf

class RoadSystem:
    intersectionGraph = []
    agents = []
    
    def __init__(self, level, box, hgtMap, lqdMap, origo):
        print("startPos: ", origo)
        self.level = level
        self.origo = origo
        self.width = box.width
        self.height = box.length
        self.heightMap = hgtMap
        self.liquidMap = lqdMap
        self.roadMap = [[0 for x in range(self.width)] for z in range(self.height)]
        self.roadGraph = Graph.Graph(box.width, box.length)
        self.roadGraph.createDiagOrthogonalGraphFrom2D(self.roadMap)
        self.intersectionGraph.append([])
        self.SetRoadMapTile(self.width/2,self.height/2)
      
    def CreateAgents(self, nrAgents):
        for i in range(nrAgents):
            self.agents.append(ExtendorAgent(self, Vector(len(self.heightMap[0])/2, len(self.heightMap)/2)))
        
    def UpdateAgents(self):
        for a in self.agents:
            a.Act()
        
    def Analyze(self, suggestion):
        self.CreateRoad(suggestion)
        
    def CreateRoad(self, suggestion):
        for p in suggestion:
            self.SetRoadMapTile(p[0],p[1])
            
    def SetRoadMapTile(self, X, Y):
        self.roadMap[Y][X] = 99
        uf.setBlock(self.level, (35,1), int(self.origo.x + X), self.heightMap[Y][X], int(self.origo.y + Y ))
        self.SpreadRoadCoverage(5, X, Y)
        
    def SpreadRoadCoverage(self, value, X, Y):
        if value == 0:
            return
        if X < 0 or Y < 0 or X >= self.width or Y >= self.height:
            return
        
        topFree = Y-1 >= 0
        leftFree = X-1 >= 0
        botFree = Y+1 < self.height
        rightFree = X+1 < self.width
        if leftFree:
            self.roadMap[Y][X-1] = max(self.roadMap[Y][X-1], value)
            self.SpreadRoadCoverage(value-1,X-1,Y)
        if leftFree and topFree:
            self.roadMap[Y-1][X-1] = max(self.roadMap[Y-1][X-1], value)
            self.SpreadRoadCoverage(value-1,X-1,Y-1)
        if topFree:
            self.roadMap[Y-1][X] = max(self.roadMap[Y-1][X], value)
            self.SpreadRoadCoverage(value-1,X,Y-1)
        if topFree and rightFree:
            self.roadMap[Y-1][X+1] = max(self.roadMap[Y-1][X+1], value)
            self.SpreadRoadCoverage(value-1,X+1,Y-1)
        if rightFree:
            self.roadMap[Y][X+1] = max(self.roadMap[Y][X+1], value)
            self.SpreadRoadCoverage(value-1,X+1, Y)
        if botFree and rightFree:
            self.roadMap[Y+1][X+1] = max(self.roadMap[Y+1][X+1], value)
            self.SpreadRoadCoverage(value-1,X+1,Y+1)
        if botFree:
            self.roadMap[Y+1][X] = max(self.roadMap[Y+1][X], value)
            self.SpreadRoadCoverage(value-1,X, Y+1)
        if botFree and leftFree:
            self.roadMap[Y+1][X-1] = max(self.roadMap[Y+1][X-1], value)
            self.SpreadRoadCoverage(value-1,X-1,Y+1)
        
class ExtendorAgent:
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 1.0
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.blockPos = Vector(0,0)
        self.dir = Vector(1,0)
        self.dir.rotate_ip(Random.randint(0,359))
        
    def Act(self):
        if not self.Move():
            return
        #self.TraceTraveledPath()
        if self.Analyze():
            self.Suggest()
    
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
        if self.roadSystem.roadMap[int(self.pos.y)][int(self.pos.x)] == 0:
            self.MakeRoad()
            
    '''follow roadmap distance to existing road and log every step'''
    def MakeRoad(self):
        path = []
        path.append([int(self.pos.x), (int(self.pos.y))])
        while True:
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
            path.append([nextX,nextY])
        while len(path) != 0:
            pos = path.pop()
            placeX = pos[0]
            placeY = pos[1]
            self.roadSystem.SetRoadMapTile(placeX, placeY)
        
        
    def CheckValue(self, X, Y, value):
        value = self.roadSystem.roadMap[Y][X]
        nextX = X
        nextY = Y
        return value, nextX, nextY
        #weighted BFS where higher weights is more attractive
        #untill it reaches a weight "roadWeight"
        
    # def CreateMinSpanTree(self, start):
    #     enqueued = [False for i in range(self.roadSystem.roadGraph.NrNodes())]
    #     minSpanTree = [-1 for i in range(self.roadSystem.roadGraph.NrNodes())]
    #     queue = Queue.Queue()
    #     queue.put(start)
    #     enqueued[start] = True
    #     while(len(queue) > 0):
    #         activeNode = queue.get()
    #         if(self.roadSystem.roadGraph[activeNode].weight == 99):
    #             break
    #         for e in self.roadSystem.roadGraph[activeNode]:
    #             toIndex = e
    #             if(not enqueued[toIndex]):
    #                 enqueued[toIndex] = True
    #                 minSpanTree[toIndex] = activeNode
    #                 queue.put(toIndex)
    #     return (activeNode, minSpanTree)
    
    # def BFS(self, start):
    #
    #     #path = []
    #     #minSpanTreeData = CreateMinSpanTree(start)
    #     minSpanTree = minSpanTreeData[1]
    #     goal = minSpanTreeData[0]
    #     nodeID = goal
    #     while(nodeID != start):
    #         path.append(nodeID)
    #         nodeID = minSpanTree[nodeID]
    #     path.append(start)
    #     return path
        
    
    
    
    
    
    
    
    
    
    