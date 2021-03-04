# -*- coding: utf-8 -*-
"""
Created on Thur Mar  4 10:37:34 2021

@author: Albin Esko
"""
import utilityFunctions as uf
import random as rand
import numpy as np
from scipy.spatial.transform import Rotation as R
from pymclevel import alphaMaterials
inputs = (
        ("Tokens", 10),
        ("Radius", 3),
        ("Material", alphaMaterials.Cobblestone), 
        )

def perform(level, box, options):
    x = RidgeAgent(options["Tokens"], [box.minx + box.width/2,0,box.minz + box.height/2], [1,0,0], options["Radius"])
    while not x.IsDone():
        x.Act(level,box,options)
    
class RidgeAgent:
    # int startTokens, vector3 pos, vector3 dir, int radius
    def __init__(self, startTokens, pos, dir, radius):
        self.tokens = startTokens
        self.pos = pos
        self.dir = dir
        self.radius= radius
        
    def Act(self, level, box, options):
        self.PlaceBlocks(level, box, options)
        self.Move(box)
        
    def PlaceBlocks(self, level, box, options):
        for x in range(int(self.pos[0]-self.radius),int(self.pos[0]+self.radius)):
            for z in range(int(self.pos[2]-self.radius), int(self.pos[2]+self.radius)):
                for y in range(box.maxy-1, box.miny-1, -1):
                    if(level.blockAt(x,y,z) != 0):
                        uf.setBlock(level,(options["Material"].ID, options["Material"].blockData),x,y+1,z)
                        break
        self.tokens = self.tokens - 1
        
    def Move(self, box):
        self.pos[0] = self.dir[0] + self.pos[0]
        self.pos[1] += self.dir[1]
        self.pos[2] += self.dir[2]
        print(self.pos)
        r = rand.random()
        if r < 0.80:
            print("No dir change")
        elif r < 0.90:
            vec = self.dir
            rotation_degrees = -45
            rotation_radians = np.radians(rotation_degrees)
            rotation_axis = np.array([0, 1, 0])
            rotation_vector = rotation_radians * rotation_axis
            rotation = R.from_rotvec(rotation_vector)
            rotated_vec = rotation.apply(vec)
            rotated_vec[0] = round(rotated_vec[0])
            rotated_vec[1] = round(rotated_vec[1])
            rotated_vec[2] = round(rotated_vec[2])
            self.dir = rotated_vec
            print("turned Right")
            print(self.dir)
        else:
            vec = self.dir
            rotation_degrees = 45
            rotation_radians = np.radians(rotation_degrees)
            rotation_axis = np.array([0, 1, 0])
            rotation_vector = rotation_radians * rotation_axis
            rotation = R.from_rotvec(rotation_vector)
            rotated_vec = rotation.apply(vec)
            rotated_vec[0] = round(rotated_vec[0])
            rotated_vec[1] = round(rotated_vec[1])
            rotated_vec[2] = round(rotated_vec[2])
            self.dir = rotated_vec
            print("turned Left")
            print(self.dir)
            
    def IsDone(self):
        return self.tokens <= 0