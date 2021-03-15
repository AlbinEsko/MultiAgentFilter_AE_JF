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
    diffThresh = 2
    H = len(nodes)
    W = len(nodes[0])
    print(H,W)
    visited = [False for i in range(W*H)]
    region = []
    stack = []
    #print("start find regions")
    while(not all(visited)):
        start = findStartNode(H,W,visited) #loops through visited 2d bool array to find a false then return that pos
        #print("Start of new region: ", start)
        stack.append(start)
        visited[start] = True #set start pos as visited
        while(len(stack) != 0):
            currentNode = stack.pop()
            region.append([currentNode % W, currentNode / W])
            #print(currentNode % W, currentNode / W)
            for i in graph[currentNode]:
                nextNode = i[0]
                weight = i[1]
                print(nextNode , weight)
                if(abs(weight) > diffThresh):
                    continue
                if(not visited[nextNode]):
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
 
'''
def test():
    array = [[random.choice((0,1,2,3,4,5,6,7,8,9)) for i in range(10)] for j in range(15)]
    connectedNodes = connectivity(array)
    #print(connectedNodes)
    for r in connectedNodes:
        print(r)
        print(len(r))

    
test()
'''