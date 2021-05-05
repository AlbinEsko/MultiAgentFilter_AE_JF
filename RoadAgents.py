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
            #print ("road construction aborted")
            return
        data = d.pathTo(to)
        path = Road.Path(data, self.roadSystem.width)
        if path.isEmpty():
            return
        self.pos = path.getLastCoord()
        self.dir.rotate_ip(Random.randint(0,359))
        self.roadSystem.Analyze(path)
        
class ConnectorAgent:
    
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 1
        self.pos = Vector(float(startPos.x), float(startPos.y))
        self.blockPos = Vector(0,0)
        self.dir = Vector(1,0)
        self.dir.rotate_ip(Random.randint(0,7)*45)
    
    
    def Move(self):
        oldPos = self.pos
        #has direction
        #scan all surounding tiles, 
        #then pick one which doesnt double back unless neccecary, calced throug dir
        #make move and set new dir (new pos - old pos)
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    