# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial.transform import Rotation as R

class RoadSystem:
    RoadArray = []
    RoadGraph = []
    
    def __init__(self, level, box, hgtMap, lqdMap, startPos):
        self.heightMap = hgtMap
        self.liquidMap = lqdMap
        self.RoadArray = [[0 for x in range(box.width)] for z in range(box.length)]
        self.RoadGraph.append([])
        
    def Analyze(self, suggestion):
        CreateRoad(suggestion)
        
    def CreateRoad(self, suggestion):
        for p in suggestion:
            self.RoadArray[p[1]][p[0]] = 99
        
class ExtendorAgent:
    def __init__(self, rodMap, hgtMap, lqdMap, startPos, roadSystem):
        self.roadMap = rodMap
        self.heightMap = hgtMap
        self.liquidMap = lqdMap
        self.pos = startPos
        self.speed = 1
        self.dir = [1,0,0]
        self.roadSystem = roadSystem
        
    def Act(self):
        Move()
        if Analyze():
            Suggest()
    
    '''Wander around 
    Keep close to existing roads'''
    def Move(self):
        self.pos[0] += self.dir[0] * speed
        self.pos[1] += self.dir[1] * speed
        self.pos[2] += self.dir[2] * speed
    
    def Turn(self, CCWdegrees = 0, axis = [0,1,0]):
        vec = self.dir
        rotation_radians = np.radians(degrees)
        rotation_axis = np.array(axis)
        rotation_vector = rotation_radians * rotation_axis
        rotation = R.from_rotvec(rotation_vector)
        rotated_vec = rotation.apply(vec)
        rotated_vec[0] = round(rotated_vec[0])
        rotated_vec[1] = round(rotated_vec[1])
        rotated_vec[2] = round(rotated_vec[2])
        self.dir = rotated_vec
    
    '''Analyze current position for road coverage'''
    def Analyze(self):
        if self.roadMap[self.pos[2]][self.pos[0]] == 0:
            Suggest()
    '''follow roadmap distance to existing road and log every step'''
    def Suggest(self):
        