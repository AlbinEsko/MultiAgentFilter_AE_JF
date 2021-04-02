# -*- coding: utf-8 -*-
import numpy as np
import random as Random
from scipy.spatial.transform import Rotation as R
from pygame.math import Vector2 as Vector
import Graph as Graph
import queue as Queue
import utilityFunctions as uf

class RoadSystem:
    intersectionGraph = []
    agents = []
    
    def __init__(self, level, box, hgtMap, lqdMap, origo):
        print("startPos: ", origo)
        self.level = level
        self.origo = origo
        self.heightMap = hgtMap
        self.liquidMap = lqdMap
        self.roadMap = [[0 for x in range(box.width)] for z in range(box.length)]
        self.roadGraph = Graph.Graph(box.width, box.length)
        self.roadGraph.createDiagOrthogonalGraphFrom2D(self.roadMap)
        self.intersectionGraph.append([])
      
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
            self.roadMap[p[1]][p[0]] = 99
        
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
        self.TraceTraveledPath()
        #if Analyze():
        #    Suggest()
    
    '''Wander around 
    Keep close to existing roads'''
    def Move(self):
        oldPos = self.pos
        self.pos += self.dir * self.speed
        self.dir.rotate_ip(Random.randint(-10,10)) #Needs improvement for the wanted wandering behavior; move to roadMap values of zero
        return self.ConvertToBlock(self.pos) == self.ConvertToBlock(oldPos)
    
    def ConvertToBlock(self, p):
        blockPos = Vector(int(p.x),int(p.y))
        return blockPos
    
    def TraceTraveledPath(self):
        uf.setBlock(self.roadSystem.level, (35,0), int(self.roadSystem.origo.x + self.pos.x), self.roadSystem.heightMap[int(self.pos.y)][int(self.pos.x)], int(self.roadSystem.origo.y + self.pos.y ))
    
    '''Analyze current position for road coverage'''
    def Analyze(self):
        if self.roadMap[int(self.pos.y)][int(self.pos.x)] == 0:
            Suggest()
            
    '''follow roadmap distance to existing road and log every step'''
    def Suggest(self):
        path = BFS(self.pos)
        #weighted BFS where higher weights is more attractive
        #untill it reaches a weight "roadWeight"
        
    def CreateMinSpanTree(self, start):
        enqueued = [False for i in range(self.roadSystem.roadGraph.NrNodes())]
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
                if(not enqueued[toIndex]):
                    enqueued[toIndex] = True
                    minSpanTree[toIndex] = activeNode
                    queue.put(toIndex)
        return (activeNode, minSpanTree)
    
    def BFS(self, start):
        path = []
        minSpanTreeData = CreateMinSpanTree(start)
        minSpanTree = minSpanTreeData[1]
        goal = minSpanTreeData[0]
        nodeID = goal
        while(nodeID != start):
            path.append(nodeID)
            nodeID = minSpanTree[nodeID]
        path.append(start)
        return path
        
    
    
    
    
    
    
    
    
    
    