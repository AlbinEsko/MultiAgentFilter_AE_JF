# -*- coding: utf-8 -*-
import numpy as np
import random as Random
from scipy.spatial.transform import Rotation as R
from pygame.math import Vector2 as Vector

import queue as Queue

class RoadSystem:
    roadMap = []
    roadGraph = []
    intersectionGraph = []
    agents = []
    
    def __init__(self, level, box, hgtMap, lqdMap, startPos):
        self.heightMap = hgtMap
        self.liquidMap = lqdMap
        self.roadMap = [[0 for x in range(box.width)] for z in range(box.length)]
        self.roadGraph = Graph.MakeGraph(box.width * box.length)
        self.intersectionGraph.append([])
        agents.append(ExtendorAgent(self, startPos))
        
    def Analyze(self, suggestion):
        CreateRoad(suggestion)
        
    def CreateRoad(self, suggestion):
        for p in suggestion:
            self.roadMap[p[1]][p[0]] = 99
        
class ExtendorAgent:
    pos = Vector()
    dir = Vector()
    speed = 0.0
    def __init__(self, roadSystem, startPos):
        self.roadSystem = roadSystem
        self.speed = 1.0
        self.pos = Vector(1,0)
        self.dir = Vector(1,0)
        self.dir.rotate(Random.randint(0,359))
        
    def Act(self):
        if not Move():
            return
        if Analyze():
            Suggest()
    
    '''Wander around 
    Keep close to existing roads'''
    def Move(self):
        oldPos = self.pos
        self.pos += self.dir * self.speed
        self.dir.rotate(Random.randint(-10,10)) #Needs improvement for the wanted wandering behavior; move to roadMap values of zero
        return ConvertToBlock(pos) == ConvertToBlock(oldPos)
    
    def ConvertToBlock(self):
        blockPos = self.pos
        blockPos.x = round(blockPos.x)
        blockPos.y = round(blockPos.y)
        return blockPos

    
    '''Analyze current position for road coverage'''
    def Analyze(self):
        if self.roadMap[int(self.pos.y)][int(self.pos.x)] == 0:
            Suggest()
            
    '''follow roadmap distance to existing road and log every step'''
    def Suggest(self):
        #weighted BFS where higher weights is more attractive
        #untill it reaches a weight "roadWeight"
        
    def CreateMinSpanTree(self, start):
        enqueqed = [False for i in range(self.roadSystem.roadGraph.NrNodes())]
        minSpanTree = [-1 for i in range(self.roadSystem.roadGraph.NrNodes())]
        queue = Queue.Queue()
        queue.put(start)
        enqueued[start] = True
        while(len(queue) > 0):
            activeNode = queue.get()
            if(self.roadSystem.roadGraph[activeNode].weight == roadWeight):
                break
            for e in self.roadSystem.roadGraph[activeNode]:
                toIndex = e
                if(!enqueued[toIndex]):
                    enqueued[toIndex] = True
                    minSpanTree[toIndex] = activeNode
                    queue.put(toIndex)
        return (activeNode, minSpanTree)
    
    def BFS(self, start):
        path = []
        minSpanTree = CreateMinSpanTree(start)
        
    
    
    
    
    
    
    
    
    
    