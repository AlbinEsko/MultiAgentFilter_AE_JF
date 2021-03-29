# -*- coding: utf-8 -*-
from array import *
import random

class Graph:
    def __init__(self, w, h, weighted = False, withDiagonals = False):
        self.graph = [[] for i in range(w*h)]
        self.width = w
        self.height = h
        
    def __getitem__(self,index):#overloaded operator[]
        return self.graph[index]
    
    def get_NrNodes(self):
        return len(self.graph)
    
    def createOrthogonalGraphFrom2D(self, data):
        for z in range(self.height):
            for x in range(self.width):
                if(z > 0):#Up
                    self.graph[x+z*self.width].append(DirectedEdge(x + (z-1) * self.width, data[z-1][x]-data[z][x]))
                if(z < self.height-1):#Down
                    self.graph[x+z*self.width].append(DirectedEdge(x + (z+1) * self.width, data[z+1][x]-data[z][x]))
                if(x > 0):#Left
                    self.graph[x+z*self.width].append(DirectedEdge((x-1) + z * self.width, data[z][x-1]-data[z][x]))
                if(x < self.width-1):#Right
                    self.graph[x+z*self.width].append(DirectedEdge((x+1) + z * self.width, data[z][x+1]-data[z][x]))
        return self.graph

    def createDiagOrthogonalGraphFrom2D(self, data):
        for z in range(self.height):
            for x in range(self.width):
                if(z > 0):#Up
                    self.graph[x+z*self.width].append(DirectedEdge(x + (z-1) * self.width, data[z-1][x]-data[z][x]))
                if(z < self.height-1):#Down
                    self.graph[x+z*self.width].append(DirectedEdge(x + (z+1) * self.width, data[z+1][x]-data[z][x]))
                if(x > 0):#Left
                    self.graph[x+z*self.width].append(DirectedEdge((x-1) + z * self.width, data[z][x-1]-data[z][x]))
                if(x < self.width-1):#Right
                    self.graph[x+z*self.width].append(DirectedEdge((x+1) + z * self.width, data[z][x+1]-data[z][x]))
                    
                if(z > 0 and x > 0):#Up left
                    self.graph[x+z*self.width].append(DirectedEdge((x-1) + (z-1) * self.width, data[z-1][x-1]-data[z][x]))
                if(z > 0 and x < self.width-1):#Up Right
                    self.graph[x+z*self.width].append(DirectedEdge((x+1) + (z-1) * self.width, data[z-1][x+1]-data[z][x]))
                if(z < self.height-1 and x > 0):#Down Left
                    self.graph[x+z*self.width].append(DirectedEdge((x-1) + (z+1) * self.width, data[z+1][x-1]-data[z][x]))
                if(z < self.height-1 and x < self.width-1):#Down Right
                    self.graph[x+z*self.width].append(DirectedEdge((x+1) + (z+1) * self.width, data[z+1][x+1]-data[z][x]))
        return self.graph

#class Node: #currently only an integer
    
class DirectedEdge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight
def getEarliestUnvisitedNode(NrNodes, visited):
        for n in range(NrNodes):
            if(not visited[n]):
                return n
def newConnectivity(graph, heightMap, diffThresh = 3.0):   
    regions = []
    visited = [False for i in range(graph.get_NrNodes())]
    region = []
    stack = []
    while(not all(visited)):
        start = getEarliestUnvisitedNode(graph.get_NrNodes(),visited) #loops through visited 2d bool array to find a false then return that pos
        regionAvgHeight = 0.0
        stack.append(start)
        visited[start] = True #set start pos as visited
        while(len(stack) != 0):
            currentNode = stack.pop()
            regionAvgHeight = (regionAvgHeight*(len(region)) + heightMap[currentNode / graph.width][currentNode % graph.width]) / (len(region)+1)
            region.append([currentNode % graph.width, currentNode / graph.width])
            for edge in graph[currentNode]:
                nextDiff = heightMap[edge.to / graph.width][edge.to % graph.width] - regionAvgHeight
                if(abs(nextDiff) > diffThresh):
                    continue
                if(not visited[edge.to]):
                    visited[edge.to] = True
                    stack.append(edge.to)
        regions.append(region)
        region = []
        regionAvgHeight = 0.0
    return regions

def newLiquidMap(graph, liquidMap, diffThresh = 3.0):   
    regions = []
    visited = [False for i in range(graph.get_NrNodes())]
    region = []
    stack = []
    while(not all(visited)):
        start = getEarliestUnvisitedNode(graph.get_NrNodes(),visited) #loops through visited 2d bool array to find a false then return that pos
        stack.append(start)
        visited[start] = True #set start pos as visited
        while(len(stack) != 0):
            currentNode = stack.pop()
            curretType = liquidMap[currentNode / graph.width][currentNode % graph.width]
            region.append([currentNode % graph.width, currentNode / graph.width])
            for edge in graph[currentNode]:
                nextType = liquidMap[edge.to / graph.width][edge.to % graph.width]
                if (curretType != nextType):
                    continue
                if (not visited[edge.to]):
                    visited[edge.to] = True
                    stack.append(edge.to)
        regions.append(region)
        region = []
    return regions
'''
Creates a graph from a 2D array and creates connected regions with a DFS traversal
Returns: List of lists containing 2D coordinates for any region
'''

def liquidMap(nodes):
    graph = creategraph(nodes)
    regions = []
    H=len(nodes)
    W=len(nodes[0])
    visited = [False for i in range(W * H)]
    region = []
    stack = []
    while (not all(visited)):
        start = findStartNode(H, W, visited)
        stack.append(start)
        visited[start] = True
        while(len(stack) != 0):
            currentNode = stack.pop()
            curretType = nodes[currentNode / W][currentNode % W]
            region.append([currentNode % W, currentNode / W])
            for i in graph[currentNode]:
                nextNode = i[0]
                weight = i[1]
                # print(nextNode , weight)
                # if(abs(weight) > diffThresh):
                #    continue
                nextType = nodes[nextNode / W][nextNode % W]
                # print("diff ",nextDiff)
                if (curretType != nextType):
                    continue
                if (not visited[nextNode]):
                    visited[nextNode] = True
                    stack.append(nextNode)
        regions.append(region)
        region = []
    return regions

def connectivity(nodes):
    graph = creategraph(nodes)
    regions = []
    diffThresh = 3
    H = len(nodes)
    W = len(nodes[0])
    #print(H,W)
    visited = [False for i in range(W*H)]
    region = []
    stack = []
    print("start find regions")
    while(not all(visited)):
        start = findStartNode(H,W,visited) #loops through visited 2d bool array to find a false then return that pos
        regionAvgHeight = 0.0
        #print("Start of new region: ", start)
        stack.append(start)
        visited[start] = True #set start pos as visited
        while(len(stack) != 0):
            currentNode = stack.pop()
            region.append([currentNode % W, currentNode / W])
            regionAvgHeight = (regionAvgHeight*(len(region)-1) + nodes[currentNode / W][currentNode % W]) / len(region)
            #print('avgHgt ', regionAvgHeight)
            #print("pos height ", nodes[currentNode / W][currentNode % W])
            for i in graph[currentNode]:
                nextNode = i[0]
                weight = i[1]
                #print(nextNode , weight)
                #if(abs(weight) > diffThresh):
                #    continue
                nextDiff = nodes[nextNode / W][nextNode % W] - regionAvgHeight
                #print("diff ",nextDiff)
                if(abs(nextDiff) > diffThresh):
                    continue
                if(not visited[nextNode]):
                    visited[nextNode] = True
                    stack.append(nextNode)
        regions.append(region)
        #print(regionAvgHeight)
        region = []
        regionAvgHeight = 0.0
    return regions

    '''
    while any is false in visited
        pick a position with value false
        DFS with threshhold
            push all connections from first on stack
            while stack is not empty
                pop stack push all not visited connections
    '''

def findStartNode(H, W, visited):
        for x in range(W):
            for z in range(H):
                if(not visited[x + z*W]):
                    return x+z*W
    
def creategraph(nodes):
    H = len(nodes)
    W = len(nodes[0])
    #print(H,W)
    graph = [[] for i in range(W*H)] #graph[pos][0=edgeTo, 1=Weight]
    for z in range(H):
        for x in range(W):
            if(x > 0):
                graph[x+z*W].append([(x-1) + z*W, nodes[z][x-1]-nodes[z][x]])
            if(x < W-1):
                graph[x+z*W].append([(x+1) + z*W, nodes[z][x+1]-nodes[z][x]])
            if(z > 0):
                graph[x+z*W].append([x + (z-1)*W, nodes[z-1][x]-nodes[z][x]])
            if(z < H-1):
                graph[x+z*W].append([x + (z+1)*W, nodes[z+1][x]-nodes[z][x]])
    return graph
 

def test():
    W = 10
    H = 15
    array = [[random.choice((0,1,2,3,4,5,6,7,8,9)) for i in range(W)] for j in range(H)]
    graph = Graph(W,H)
    graph.createOrthogonalGraphFrom2D(array)
    regions = newConnectivity(graph, array)
    #print(connectedNodes)
    tot = 0
    for r in regions:
        print(len(r))
        tot += len(r)
    print(tot)

if __name__ == "__main__":
    test()
