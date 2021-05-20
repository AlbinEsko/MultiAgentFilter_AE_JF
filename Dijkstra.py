# -*- coding: utf-8 -*-
import sys
import numpy as np
import Graph
import BinaryHeap
class dijkstras:
    def __init__(self, graph, start):
        self.edgeTo = [None for i in range(graph.nrNodes + 1)]
        self.distTo = np.full(graph.nrNodes + 1, sys.maxint)
        self.pq = BinaryHeap.IndexMinPQ(graph.nrNodes +1, float)
        self.distTo[start] = 0
        self.pq.insert(start, 0.0)
        
    def buildCompleteMinSpanTree(self, graph):
        while not self.pq.isEmpty():
            self.relax(graph, self.pq.delMin())
      
    def relax(self, graph, v):
        edgeList = graph[v].adjacent
        for edge in edgeList:
            w = edge.to
            if self.distTo[w] > self.distTo[v] + edge.weight:
                self.distTo[w] = self.distTo[v] + edge.weight
                self.edgeTo[w] = edge
                if self.pq.contains(w):
                    self.pq.changeKey(w, self.distTo[w])
                else:
                    self.pq.insert(w, self.distTo[w])
    
    def buildOnRoadMinSpanTree(self, graph):
        while not self.pq.isEmpty():
            self.relaxOnRoad(graph, self.pq.delMin())
      
    def relaxOnRoad(self, graph, v):
        edgeList = graph[v].roadAdjacent
        for edge in edgeList:
            w = edge.to
            if self.distTo[w] > self.distTo[v] + edge.weight:
                self.distTo[w] = self.distTo[v] + edge.weight
                self.edgeTo[w] = edge
                if self.pq.contains(w):
                    self.pq.changeKey(w, self.distTo[w])
                else:
                    self.pq.insert(w, self.distTo[w])     
                    
    def buildToRoadMinSpanTree(self, graph):
        while not self.pq.isEmpty():
            nextIndex = self.pq.delMin()
            if self.relaxUntillRoad(graph, nextIndex):
                #print("road found")
                return nextIndex
        return -1

    def relaxUntillRoad(self, graph, v):
        node = graph[v]
        for edge in node.adjacent:
            w = edge.to
            if self.distTo[w] > self.distTo[v] + edge.weight:
                self.distTo[w] = self.distTo[v] + edge.weight
                self.edgeTo[w] = edge
                if self.pq.contains(w):
                    self.pq.changeKey(w, self.distTo[w])
                else:
                    self.pq.insert(w, self.distTo[w])
        if node.roadVal == 99:
            return True
        return False
                    
    def distTo(self, v):
        return self.distTo[v]
    
    def hasPathTo(self, v):
        return self.distTo[v] < sys.maxint
    
    def pathTo(self,v):
        if not self.hasPathTo(v):
            return None
        path = []
        e = self.edgeTo[v]
        while e != None:
            path.append(e)
            e = self.edgeTo[e.frm]
        return path
    
if __name__ == "__main__":
    import random
    print("test")
    W = 10
    H = 10
    array = [[random.choice([0,1,2,3,4,5,6,7,8,9]) for i in range(W)] for j in range(H)]
    graph = Graph.Graph(W, H, array, array)
    graph.createOrthogonalGraphFrom2D()
    graph.getNode(5,5).roadVal = 99
    print('created')
    d = dijkstras(graph,0)
    closestRoad = d.buildToRoadMinSpanTree(graph)
    path = d.pathTo(closestRoad)
    for e in path:
        to = e.to
        print(to%W, to/W)
        
'''random.choice((0,1,2,3,4,5,6,7,8,9))'''