# -*- coding: utf-8 -*-
import sys
import numpy as np
import Graph
import BinaryHeap
class dijkstras:
    def __init__(self, graph, start):
        self.edgeTo = np.empty(graph.get_NrNodes(), Graph.DirectedEdge)
        self.distTo = np.full(graph.get_NrNodes(), sys.maxint)
        self.pq = BinaryHeap.IndexMinPQ(graph.get_NrNodes(), float)
        self.distTo[start] = 0
        while not self.pq.isEmpty():
            self.relax(graph, self.pq.delMin())
            
    def relax(self, graph, v):
        for edge in graph[v].adjacent:
            w = edge.to
            if self.distTo[w] > self.distTo[v] + edge.weight:
                self.distTo[w] = self.distTo[v] + edge.weight
                self.edgeTo[w] = edge
                if self.pq.contains(w):
                    self.pq.changeKey(w, self.distTo[w])
                else:
                    self.pq.insert(w, self.distTo[w])
                    
    def distTo(self, v):
        return self.distTo[v]
    
    def hasPathTo(self, v):
        return self.distTo[v] < sys.maxint
    
    def pathTo(self, v):
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
    W = 10
    H = 15
    array = [[random.choice((0,1,2,3,4,5,6,7,8,9)) for i in range(W)] for j in range(H)]
    graph = Graph.Graph(W, H, array, array)
    print('created')
    d = dijkstras(graph,0)
    path = d.pathTo(H*W-1)
    for v in path:
        print(v.x, v.y)