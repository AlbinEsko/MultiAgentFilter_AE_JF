# -*- coding: utf-8 -*-

class Graph:
    def __init__(self, w, h, hgtMap, lqdMap):
        self.graph = []
        self.width = w
        self.height = h
        for y in range(h):
            for x in range(w):
                self.graph.append(Node(x,y,hgtMap[y][x], lqdMap[y][x]))
        
    def __getitem__(self,index):#overloaded operator[]
        return self.graph[index]
    
    def getNode(self,x,y):
        return self.graph[x+y*self.width]
    
    def get_NrNodes(self):
        return len(self.graph)
        
    
    def createOrthogonalGraphFrom2D(self, data):
        for y in range(self.height):
            for x in range(self.width):
                if(y > 0):#Up
                    self.graph[x+y*self.width].append(DirectedEdge(x + (y-1) * self.width, data[y-1][x]-data[y][x]))
                if(y < self.height-1):#Down
                    self.graph[x+y*self.width].append(DirectedEdge(x + (y+1) * self.width, data[y+1][x]-data[y][x]))
                if(x > 0):#Left
                    self.graph[x+y*self.width].append(DirectedEdge((x-1) + y * self.width, data[y][x-1]-data[y][x]))
                if(x < self.width-1):#Right
                    self.graph[x+y*self.width].append(DirectedEdge((x+1) + y * self.width, data[y][x+1]-data[y][x]))
        return self.graph


class Node:
    def __init__(self, x, y, height, liquid):
        self.x = x
        self.y = y
        self.adjacent = {}
        self.height = height
        self.liquid = liquid
        self.roadVal = 0
        
    def addEdge(self, to, weight = 1):
        self.adjacent[to] = weight
      
    def addEdge_xy(self, x, y, width, weight = 1):
        self.adjacent[x+y*width] = weight
        
    def changeEdgeWeight(self, edgeTo, newWeight):
        self.adjacent[edgeTo] = newWeight
                
    
        
class DirectedEdge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight

    def changeWeight(self, newWeight):
        self.weight = newWeight
        
        
def getEarliestUnvisitedNode(NrNodes, visited):
        for n in range(NrNodes):
            if(not visited[n]):
                return n
            
'''
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
            for y in range(H):
                if(not visited[x + y*W]):
                    return x+y*W
    
def creategraph(nodes):
    H = len(nodes)
    W = len(nodes[0])
    #print(H,W)
    graph = [[] for i in range(W*H)] #graph[pos][0=edgeTo, 1=Weight]
    for y in range(H):
        for x in range(W):
            if(x > 0):
                graph[x+y*W].append([(x-1) + y*W, nodes[y][x-1]-nodes[y][x]])
            if(x < W-1):
                graph[x+y*W].append([(x+1) + y*W, nodes[y][x+1]-nodes[y][x]])
            if(y > 0):
                graph[x+y*W].append([x + (y-1)*W, nodes[y-1][x]-nodes[y][x]])
            if(y < H-1):
                graph[x+y*W].append([x + (y+1)*W, nodes[y+1][x]-nodes[y][x]])
    return graph
 


if __name__ == "__main__":
    import random
    W = 10
    H = 15
    array = [[random.choice((0,1,2,3,4,5,6,7,8,9)) for i in range(W)] for j in range(H)]
    graph = Graph(W,H)
    graph.createOrthogonalGraphFrom2D(array)
    #regions = newConnectivity(graph, array)
    #print(connectedNodes)
    tot = 0
    for r in regions:
        print(len(r))
        tot += len(r)
    print(tot)
