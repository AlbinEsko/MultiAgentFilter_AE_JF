# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:34:34 2021

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
import RoadAgents
import PlottingAgents
import BlockIDs as Blocks

class RoadSystem:
    agents = []
    roadCoverage = 16
    def __init__(self, level, box, hgtMap, lqdMap, origo):
        self.level = level
        self.origo = origo
        self.width = box.width
        self.height = box.length
        self.heightMap = hgtMap
        self.liquidMap = lqdMap
        self.graph = Graph.Graph(box.width, box.length,hgtMap,lqdMap)
        self.create8WayEdges(self.graph)
        startCoords = self.FindStart()
        print("startPos: ", Vector(startCoords[0], startCoords[1]) + origo)
        self.SetRoadMapTile(startCoords[0],startCoords[1], 0)
        self.startPos = Vector(startCoords[0], startCoords[1])
        self.multiplier = 4
        self.plotAgents = []
        self.plots = []
        self.PointToVillage()
        
        
    def FindStart(self):
        regions = Graph.newConnectivity(self.graph)
        largestRegion = []
        for r in regions:
            if len(r) > len(largestRegion):
                largestRegion = r
        return Random.choice(largestRegion)
    
    def PointToVillage(self):
        boxCentre = Vector(self.origo.x + self.width/2, self.origo.y + self.height/2)
        pointDir = (self.startPos + self.origo) - boxCentre
        if pointDir.length() < 100:
            print("No arrow")
            return
        pointDir.normalize_ip()
        arrowSize = 10
        
        for i in range(arrowSize):
            uf.setBlock(self.level, (35,0), int(boxCentre.x + pointDir.x*i), self.graph.getNode(self.width/2,self.height/2).height + 6, int(boxCentre.y + pointDir.y*i))
            tipLocation = boxCentre + pointDir * i
        
        spokeDir = pointDir.rotate(160)
        for i in range(arrowSize):
            uf.setBlock(self.level, (35,0), int(tipLocation.x + spokeDir.x*i), self.graph.getNode(self.width/2,self.height/2).height + 6, int(tipLocation.y + spokeDir.y*i))
            
        spokeDir.rotate_ip(40)
        for i in range(arrowSize):
            uf.setBlock(self.level, (35,0), int(tipLocation.x + spokeDir.x*i), self.graph.getNode(self.width/2,self.height/2).height + 6, int(tipLocation.y + spokeDir.y*i))
            
    def CreateExtendors(self, nrAgents):
        for i in range(nrAgents):
            self.agents.append(RoadAgents.ExtendorAgent(self, self.startPos))
        #print("Extendors Created")
            
    def CreateConnectors(self, nrAgents):
        for i in range(nrAgents):
            self.agents.append(RoadAgents.ConnectorAgent(self, self.startPos))
    
    def CreatePloters(self, nrAgents):
        for i in range(nrAgents):
            self.plotAgents.append(PlottingAgents.PlotAgent(self, self.startPos))
    
    def UpdateAgents(self):
        for a in self.agents:
            a.Act()
            #print(a, "acted")
    
    def UpdatePlotAgents(self):
        for a in self.plotAgents:
            a.Act()
    
    def PrintPlots(self):
        c = 0
        for p in self.plots:
            p.PrintPlot(self.level, self.origo, c + 6)
            c = (c+1) % 10
    
    def Analyze(self, suggestion, data):
        start = suggestion.getFirstCoord()
        end = suggestion.getLastCoord()
        manhatDist = abs(end.x - start.x) + abs(end.y - start.y)
        #print(suggestion.totalWeight, len(suggestion.roadTiles), manhatDist * self.multiplier, suggestion.largestDiff)
        if(suggestion.totalWeight > manhatDist * self.multiplier): #some value dependent on the expeced lenth of a path
            #print("too costly road")
            return False
        if(suggestion.largestDiff > 2):
            #print("too steep section")
            return False
        self.CreateRoad(suggestion, data)
        #print("road added")
        return True
        
    def CreateRoad(self, suggestion, data):
        prevTileX=-1
        prevTileY=-1
        for tile in suggestion.roadTiles:
            self.SetRoadMapTile(tile[0],tile[1], data)
            if prevTileX != -1:
                self.graph.addRoadEdge(tile[0] + tile[1] * self.width, prevTileX + prevTileY * self.width)
                #print("creaded road edge")
            prevTileX=tile[0]
            prevTileY=tile[1]
            
    def DebugSetRoadMapTile(self, x, y, data):
        self.graph.getNode(x,y).roadVal = 99
        uf.setBlock(self.level, (35,data), int(self.origo.x + x), self.graph.getNode(x,y).height, int(self.origo.y + y ))
        self.RadiateFromPlacedRoad(x, y)
        #print("Tile and coverage set")
    
    def SetRoadMapTile(self, X, Y, data):
        self.graph.getNode(X,Y).roadVal = 99
        height = self.graph.getNode(X,Y).height
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if self.level.blockAt(int(self.origo.x + X + x), height, int(self.origo.y + Y +y)) != 0:
                    uf.setBlock(self.level, (45,0), int(self.origo.x + X + x), height, int(self.origo.y + Y + y))
                    #for i in range(3):
                        #block = self.level.blockAt(int(self.origo.x + X + x), height + i + 1, int(self.origo.y + Y +y)) 
                        #if not block in Blocks.getGrounds():
                            #uf.setBlock(self.level, (0,0), int(self.origo.x + X + x), height + i + 1, int(self.origo.y + Y + y))
        self.RadiateFromPlacedRoad(X, Y)
    
    def CleanObstructions(self):
        for t in self.graph.graph:
            if t.roadVal == 99:
                for y in (-1, 0, 1):
                    for x in (-1, 0, 1):
                        for i in range(3):
                            block = self.level.blockAt(int(self.origo.x + t.x + x), t.height + i + 1, int(self.origo.y + t.y +y)) 
                            if block != 45:
                                uf.setBlock(self.level, (0,0), int(self.origo.x + t.x + x), t.height + i + 1, int(self.origo.y + t.y + y))
    
    def RadiateFromPlacedRoad(self, X, Y):
        for i in range(self.roadCoverage):
            layer = i + 1 #does not include the origo position
            for x0 in range(layer * 2 + 1): #print top row of current layer
                y = layer
                x = x0 - layer
                self.SimpleSpreadRoadCoverage(self.roadCoverage - layer, x+X, y+Y)
                
                
            for x0 in range(layer * 2 + 1): #print bot row of current layer
                y = -layer
                x = x0 - layer
                self.SimpleSpreadRoadCoverage(self.roadCoverage - layer, x+X, y+Y)
                
            for y0 in range(layer * 2 + 1): #print right row of current layer
                y = y0-layer
                x = layer
                self.SimpleSpreadRoadCoverage(self.roadCoverage - layer, x+X, y+Y)
                
            for y0 in range(layer * 2 + 1): #print left row of current layer
                y = y0-layer
                x = -layer
                self.SimpleSpreadRoadCoverage(self.roadCoverage - layer, x+X, y+Y)
            
    
    def SimpleSpreadRoadCoverage(self, value, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        node = self.graph.getNode(x,y)
        node.roadVal = max(node.roadVal, value)
        #uf.setBlock(self.level, (35,value%2+4), int(self.origo.x + x), node.height, int(self.origo.y + y ))
    
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
                        graph.createEdge_xy(x, y, x-1, y+1, 2 + abs(graph.getNode(x-1,y+1).height-graph.getNode(x,y).height))
                if topFree and rightFree:
                    if graph.getNode(x+1,y+1).liquid == 0:
                        graph.createEdge_xy(x, y, x+1, y+1, 2 + abs(graph.getNode(x+1,y+1).height-graph.getNode(x,y).height))
                if botFree and rightFree:
                    if graph.getNode(x+1,y-1).liquid == 0:
                        graph.createEdge_xy(x, y, x+1, y-1, 2 + abs(graph.getNode(x+1,y-1).height-graph.getNode(x,y).height))
                if botFree and leftFree:
                    if graph.getNode(x-1,y-1).liquid == 0:
                        graph.createEdge_xy(x, y, x-1, y-1, 2 + abs(graph.getNode(x-1,y-1).height-graph.getNode(x,y).height))
                    


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
        firstEdge = data.pop()
        self.roadTiles.append((firstEdge.frm%width, firstEdge.frm/width))
            
    def getLastCoord(self):
        if self.isEmpty():
            raise Exception("path is empty")
        tup = self.roadTiles[len(self.roadTiles)-1]
        return Vector(tup[0], tup[1]) 
    
    def getFirstCoord(self):
        if self.isEmpty():
            raise Exception("path is empty")
        tup = self.roadTiles[0]
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
    
    
    
    
    
    
    