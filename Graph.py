# -*- coding: utf-8 -*-
from array import *
import random

def connectivity(nodes):
    graph = creategraph(nodes)
    print(graph)
    
    
def creategraph(nodes):
    H = len(nodes)
    W = len(nodes[0])
    print(H,W)
    graph = [[[] for i in range(len(nodes[0]))] for j in range(len(nodes))]
    for y in range(H):
        for x in range(W):
            if(x > 0):
                graph[y][x].append([x-1, y, nodes[y][x-1]-nodes[y][x]])
            if(x < W-1):
                graph[y][x].append([x+1, y, nodes[y][x+1]-nodes[y][x]])
            if(y > 0):
                graph[y][x].append([x, y-1, nodes[y-1][x]-nodes[y][x]])
            if(y < H-1):
                graph[y][x].append([x, y+1, nodes[y+1][x]-nodes[y][x]])
    return graph
    
def test():
    array = [[random.choice((0,1,2,3)) for i in range(10)] for j in range(10)]
    connectedNodes = connectivity(array)

    
test()