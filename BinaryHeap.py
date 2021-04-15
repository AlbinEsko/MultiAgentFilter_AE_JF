# -*- coding: utf-8 -*-

class BinaryHeap:
    def __init__(self, maxN = 0, data = None):
        self.__n = 0
        self.pq = [None]
        if maxN > 0:
            self.maxN = maxN
        
    def isEmpty(self):
        return self.__n == 0
    
    def size(self):
        return self.__n
    
    def insert(self, key):
        self.__n = self.__n+1
        self.__pq.append(key)
        self.swim(self.__n)
    
    def delMax(self):
        m = self.pq[1]
        self.exch(1,self.__n)
        self.__n = self.__n - 1
        self.pq.remove(self.__n+1)
        self.sink(1)
        return m
    
    def less(self, i, j):
        return self.pq[i] < self.pq[j]
    
    def exch(self, i, j):
        temp = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = temp
        
    def swim(self, k):
        while k > 1 and self.less(k/2, k):
            self.exch(k/2, k)
            k = k/2

    def sink(self, k):
        while 2*k <= self.__n:
            j = k*2
            if j < self.__n and self.less(j, j+1):
                j = j+1
            if not self.less(k,j):
                break
            self.exch(k, j)
            k = j
            
class IndexMinPQ:
    def __init__(self):
        self.pq = [None]