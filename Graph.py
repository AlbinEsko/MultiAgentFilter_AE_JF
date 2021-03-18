# -*- coding: utf-8 -*-
from array import *
import random
'''
Creates a graph from a 2D array and creates connected regions with a DFS traversal
Returns: List of lists containing 2D coordinates for any region
'''
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
    array = [[random.choice((0,1,2,3,4,5,6,7,8,9)) for i in range(10)] for j in range(15)]
    connectedNodes = connectivity(array)
    #print(connectedNodes)
    #for r in connectedNodes:
        #print(r)
        #print(len(r))

if __name__ == "__main__":
    test()
