# -*- coding: utf-8 -*-
from array import *
import random

def connectivity(nodes):
    graph = creategraph(nodes)
    regions = []
    diffThresh = 2
    H = len(nodes)
    W = len(nodes[0])
    print(H,W)
    visited = [[False for i in range(W)] for j in range(H)]
    region = []
    stack = []
    print("start find regions")
    while(not all(visited[0])):
        print("Start find a region")
        start = findStartNode(H,W,visited) #loops through visited 2d bool array to find a false then return that pos
        stack.append(start)
        visited[start[1]][start[0]] = True #set start pos as visited
        while(len(stack) != 0):
            currentNode = stack.pop()
            region.append(currentNode)
            for i in graph[currentNode[1]][currentNode[0]]:
                nextNode = i
                print(nextNode)
                print("###")
                #print(graph[nextNode[1]][nextNode[0]])
                if(nextNode[2] > diffThresh):
                    continue
                if(not visited[nextNode[1]][nextNode[0]]):
                    visited[nextNode[1]][nextNode[0]] = True
                    stack.append([nextNode[1],nextNode[0]])
        regions.append(region)
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
                if(not visited[z][x]):
                    return [x,z]
    
    
def creategraph(nodes):
    H = len(nodes)
    W = len(nodes[0])
    #print(H,W)
    graph = [[[] for i in range(W)] for j in range(H)]
    for z in range(H):
        for x in range(W):
            if(x > 0):
                graph[z][x].append([x-1, z, nodes[z][x-1]-nodes[z][x]])
            if(x < W-1):
                graph[z][x].append([x+1, z, nodes[z][x+1]-nodes[z][x]])
            if(z > 0):
                graph[z][x].append([x, z-1, nodes[z-1][x]-nodes[z][x]])
            if(z < H-1):
                graph[z][x].append([x, z+1, nodes[z+1][x]-nodes[z][x]])
    return graph
    
def test():
    array = [[random.choice((0,1,2,3)) for i in range(10)] for j in range(10)]
    connectedNodes = connectivity(array)
    print(connectedNodes)
    for r in connectedNodes:
        print(r)

    
test()