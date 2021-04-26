# -*- coding: utf-8 -*-
import sys
import heapq
import numpy as np
import random as Random
from pygame.math import Vector2 as Vector
import Graph as Graph
import Dijkstra
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
        self.graph = Graph.Graph(box.width, box.length,hgtMap,lqdMap)
        self.create8WayEdges(self.graph)
        self.intersectionGraph.append([])
        self.SetRoadMapTile(self.width/2,self.height/2)
      
    def CreateAgents(self, nrAgents):
        for i in range(nrAgents):
            self.agents.append(ExtendorAgent(self, Vector(len(self.heightMap[0])/2, len(self.heightMap)/2)))
        
    def UpdateAgents(self):
        for a in self.agents:
            a.Act()
        
    def Analyze(self, suggestion):
        if(suggestion.totalWeight > 10): #some value dependent on the expeced lenth of a path
            return
        if(suggestion.largestDiff > 3):
            return
        self.CreateRoad(suggestion)
        
    def CreateRoad(self, suggestion):
        for tile in suggestion.roadTiles:
            self.SetRoadMapTile(tile[0],tile[1])
            
    def SetRoadMapTile(self, x, y):
        self.graph.getNode(x,y).roadVal = 99
        uf.setBlock(self.level, (35,1), int(self.origo.x + x), self.graph.getNode(x,y).height, int(self.origo.y + y ))
        self.SpreadRoadCoverage(5, x, y)
        
    def SpreadRoadCoverage(self, value, X, Y):
        if value == 0:
            return
        if X < 0 or Y < 0 or X >= self.width or Y >= self.height:
            return
        
        topFree = Y+1 < self.height
        botFree = Y-1 >= 0
        leftFree = X-1 >= 0
        rightFree = X+1 < self.width
        if topFree:
            self.graph.getNode(X,Y+1).roadVal = max(self.graph.getNode(X,Y+1).roadVal, value)
            self.SpreadRoadCoverage(value-1,X,Y+1)
        if botFree:
            self.graph.getNode(X,Y-1).roadVal = max(self.graph.getNode(X,Y-1).roadVal, value)
            self.SpreadRoadCoverage(value-1,X, Y-1)
        if leftFree:
            self.graph.getNode(X-1,Y).roadVal = max(self.graph.getNode(X-1,Y).roadVal, value)
            self.SpreadRoadCoverage(value-1,X-1,Y)
        if rightFree:
            self.graph.getNode(X+1,Y).roadVal = max(self.graph.getNode(X+1,Y).roadVal, value)
            self.SpreadRoadCoverage(value-1,X+1, Y)
        if leftFree and topFree:
            self.graph.getNode(X-1,Y+1).roadVal = max(self.graph.getNode(X-1,Y+1).roadVal, value)
            self.SpreadRoadCoverage(value-1,X-1,Y+1)
        if topFree and rightFree:
            self.graph.getNode(X+1,Y+1).roadVal = max(self.graph.getNode(X+1,Y+1).roadVal, value)
            self.SpreadRoadCoverage(value-1,X+1,Y+1)
        if botFree and rightFree:
            self.graph.getNode(X+1,Y-1).roadVal = max(self.graph.getNode(X+1,Y-1).roadVal, value)
            self.SpreadRoadCoverage(value-1,X+1,Y-1)
        if botFree and leftFree:
            self.graph.getNode(X-1,Y-1).roadVal = max(self.graph.getNode(X-1,Y-1).roadVal, value)
            self.SpreadRoadCoverage(value-1,X-1,Y-1)
    
    def create8WayEdges(self, graph):
        for y in range(graph.height):
            for x in range(graph.width):
                topFree = y+1 < self.height
                botFree = y-1 >= 0
                leftFree = x-1 >= 0
                rightFree = x+1 < self.width
                if topFree:
                    if graph.getNode(x,y+1).liquid == 0:
                        graph.createEdge_xy(x, y, x, y+1, 1 + abs(graph.getNode(x,y+1).height-graph.getNode(x,y).height))
                if botFree:
                    if graph.getNode(x,y-1).liquid == 0:
                        graph.createEdge_xy(x, y, x, y-1, 1 + abs(graph.getNode(x,y-1).height-graph.getNode(x,y).height))
                if leftFree:
                    if graph.getNode(x-1,y).liquid == 0:
                        graph.createEdge_xy(x, y, x-1, y, 1 + abs(graph.getNode(x-1,y).height-graph.getNode(x,y).height))
                if rightFree:
                    if graph.getNode(x+1,y).liquid == 0:
                        graph.createEdge_xy(x, y, x+1, y, 1 + abs(graph.getNode(x+1,y).height-graph.getNode(x,y).height))
                if leftFree and topFree:
                    if graph.getNode(x-1,y+1).liquid == 0:
                        graph.createEdge_xy(x, y, x-1, y+1, 1 + abs(graph.getNode(x-1,y+1).height-graph.getNode(x,y).height))
                if topFree and rightFree:
                    if graph.getNode(x+1,y+1).liquid == 0:
                        graph.createEdge_xy(x, y, x+1, y+1, 1 + abs(graph.getNode(x+1,y+1).height-graph.getNode(x,y).height))
                if botFree and rightFree:
                    if graph.getNode(x+1,y-1).liquid == 0:
                        graph.createEdge_xy(x, y, x+1, y-1, 1 + abs(graph.getNode(x+1,y-1).height-graph.getNode(x,y).height))
                if botFree and leftFree:
                    if graph.getNode(x-1,y-1).liquid == 0:
                        graph.createEdge_xy(x, y, x-1, y-1, 1 + abs(graph.getNode(x-1,y-1).height-graph.getNode(x,y).height))
                    
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
        if self.roadSystem.graph.getNode(int(self.pos.x),int(self.pos.y)).roadVal == 0:
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
            print(value, nextX, nextY)
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
      
    #def MakeGoodRoad(self):
        #2 different weight values, Height difference and deviation from shortest
        #Bad: takes a long winding road to have no height difference
        #Bad: makes the shortest road extention possible with no regard for height difference
        #Good but shortsighted: takes the lowest weight among equaly close options
        #Good but shortsighted: takes the closest option of equaly weighed options
        #Requirement: never takes a path with a height difference larger than 1
        #improvement: allow terraforming to take shorter roads
        #weights/costs: 1 for moving horizontaly, +1 per height movement, +1 per terraform

        

    def dijkstra(self):
        #creatiing full arrays for the whole area feels wastefull, further research for later
        start = int(self.pos.x) + int(self.pos.y) * self.roadSystem.width
        if start >= self.roadSystem.graph.nrNodes:
            raise Exception("agent out of bounds at ", start, self.pos, int(self.pos.x), int(self.pos.y), self.roadSystem.width)
        d = Dijkstra.dijkstras(self.roadSystem.graph, start)
        to = d.buildToRoadMinSpanTree(self.roadSystem.graph)
        if to == -1:
            print ("road construction aborted")
            return
        data = d.pathTo(to)
        path = Path(data, self.roadSystem.width)
        if path.isEmpty():
            return
        self.pos = path.getLastCoord()
        self.dir.rotate_ip(Random.randint(0,359))
        self.roadSystem.Analyze(path)

class Path:
    def __init__(self, data, width):
        #data is a list of directedEdges
        self.totalWeight = 0
        self.roadTiles = []
        self.largestDiff = 0
        for e in data:
            self.roadTiles.append((e.to%width, e.to/width))
            self.totalWeight += e.weight
            self.largestDiff = max(self.largestDiff, e.weight)
            
    def getLastCoord(self):
        if self.isEmpty():
            raise Exception("path is empty")
        tup = self.roadTiles[len(self.roadTiles)-1]
        return Vector(tup[0], tup[1]) 
    
    def isEmpty(self):
        return len(self) == 0
    
    def __len__(self):
        return len(self.roadTiles)

def edgesToXY(path, width):
    xy_path = []
    
    return xy_path
    
def transIndToXY(i, width):
    return [i % width, i / width]
    
    
    
    
    
    
    