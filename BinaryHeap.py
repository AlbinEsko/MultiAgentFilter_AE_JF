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
            
            
import numpy as np
class IndexMinPQ:
    def __init__(self, maxSize, dtype):
        self.maxSize = maxSize
        self.n = 0
        self.pq = np.zeros(maxSize + 1, int)
        self.qp = np.full(maxSize + 1, -1)
        self.keys = np.zeros(maxSize + 1, dtype)
        
    def validateIndex(self,i):
        if(i < 0):
            raise Exception("Index is negative", i)
        if(i >= self.maxSize + 1):
            raise Exception("Index is out of bounds", i)
        return True
        
    def insert(self, i, key):
        self.validateIndex(i)
        if self.contains(i):
            raise Exception("Index " + i + " is already in the priority queue")
        self.n = self.n + 1
        self.qp[i] = self.n
        self.pq[self.n] = i
        self.keys[i] = key
        self.swim(self.n)
        
    def changeKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i):
            raise Exception("Index '" + i + "' is not in the priority queue")
        self.keys[i] = key
        self.swim(self.qp[i])
        self.sink(self.qp[i])
        return
        
    def contains(self, i):
        return self.qp[i] != -1
    
    def delete(self, i):
        self.validateIndex(i)
        if not self.contains(i):
            raise Exception("Index '" + i + "' is not in the priority queue")
        index = self.qp[i]
        self.exch(index, self.n)
        self.n = self.n - 1
        self.swim(index)
        self.sink(index)
        self.keys[i] = None
        self.qp[i] = -1
        return
    
    def minKey(self):
        if self.n == 0:
            raise Exception("priority queue is empty")
        return self.keys[self.pq[1]]
    
    def minIndex(self):
        if self.n == 0:
            raise Exception("priority queue is empty")
        return self.pq[1]
    
    def delMin(self):
        if self.n == 0:
            raise Exception("priority queue is empty")
        indexOfMin = self.pq[1]
        self.exch(1, self.n)
        self.n = self.n - 1
        self.sink(1)
        if indexOfMin != self.pq[self.n + 1]:
            raise Exception("Error in swap")
        self.qp[indexOfMin] = -1
        self.keys[self.pq[self.n + 1]] = None
        self.pq[self.n+1] = -1
        return indexOfMin
    
    def isEmpty(self):
        return self.n == 0
    
    def isFull(self):
        return self.n == self.maxSize
    
    def size(self):
        return self.n
    
    def keyOf(self, i):
        self.validateIndex(i)
        if not self.contains(i):
            raise Exception("Index '" + i + "' is not in the priority queue")
        return self.keys[self.pq[i]]
        
    def swim(self, k):
        while k > 1 and self.greater(k/2, k):
            self.exch(k/2, k)
            k = k/2
            
    def sink(self, k):
        while 2*k <= self.n:
            j = k*2
            if j < self.n and self.greater(j, j+1):
                j = j+1
            if not self.greater(k,j):
                break
            self.exch(k, j)
            k = j
            
    def exch(self, i, j):
        temp = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = temp
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j
        
    def greater(self, i, j):
        return self.keys[self.pq[i]] > self.keys[self.pq[j]]
       
if __name__ == "__main__":
    pq = IndexMinPQ(10, float)
    i = 1
    key = 5
    while not pq.isFull():
        pq.insert(i, key)
        i = i + 1
        key = (key + 1) % 10
        
    while not pq.isEmpty():
        print(pq.minKey() ,pq.delMin())