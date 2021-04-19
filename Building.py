from pymclevel import BoundingBox, MCLevel
from collections import namedtuple
import random as random
from MAF_Utility import Direction

_expansion = namedtuple("_expansion", ("n", "e", "s", "w"))


class Building():
    def __init__(self, yard, level, heightmap):
        # type: (BoundingBox, MCLevel, List[List[int]]) -> None
        print("Building")
        self.yard = yard
        self.level = level
        self.heightmap = heightmap
        self.modules = [BoundingBox]
        self.doors = []
        self.windows = []
        self.sizexmin = 5
        self.sizexmax = 10
        self.sizezmin = 5
        self.sizezmax = 10
        self.sizey = 5


class House(Building):
    def __init__(self, ):
        super(House, self).__init__()

    def generate(self, nr_of_modules):
        # type: (int) -> House
        self.create_modules(nr_of_modules)

    def create_modules(self, nr_of_modules):
        # type: (int) -> None
        for x in range(nr_of_modules):
            if x == 1:
                originx = random.randrange(0, 5)
                originz = random.randrange(0, 5)
            else:
                r = random.random()
                if r < 0.50:
                    originx = self.modules[x - 1].size.x
                    originz = random.randrange(0, 5)
                else:
                    originx = random.randrange(0, 5)
                    originz = self.modules[x - 1].size.z

            originy = self.heightmap[originz][originx]  # this needs to be checked, might need to be inverted.
            origin = [originx, originy, originz]  # lowest x,y,z of box
            sizex = random.randrange(self.sizexmin, self.sizexmax)
            sizey = self.sizey
            sizez = random.randrange(self.sizezmin, self.sizezmax)
            size = [sizex, sizey, sizez]
            module = BoundingBox(origin, size)
            self.modules.append(BoundingBox)


class Module():
    """A module is a rectangle body of a building seen from above."""

    def __init__(self, yard, box, level, building):
        # type: (BoundingBox, BoundingBox, MCLevel, Building) -> None
        self.yard = yard
        self.box = box
        self.level = level
        self.building = building
        self._expansion = self.getexpansionlimit()

    def getexpansionlimit(self, direction):
        # type: (Direction) -> List[int]
        output = []
        offset = self.box.origin - self.yard.origin
       #offsetz = self.box.origin - self.yard.origin
        height = self.box.origin.y
        if direction == Direction.NONE or direction == Direction.NORTH:
            dist = abs(self.yard.origin.z - self.box.origin.z)
            if dist != 0:
                #perpendicular to direction
                for perpendicular in range(self.box.size.x):
                    for parallel in range(dist):
                        z = (self.box.origin.z-1) - parallel
                        x = self.box.origin.x + perpendicular
                        if height != self.building.heightmap[z][x] and dist < parallel:
                            dist = parallel
                            break


            output.append(dist)
        if direction == Direction.NONE or direction == Direction.EAST:
            dist = abs((self.yard.origin.x + self.yard.size.x) - (self.box.origin.x + self.box.size.x))
            if dist != 0:
                for perpendicular in range(self.box.size.z):
                    for parallel in range(dist):
                        z= self.origin.z + perpendicular
                        x= (self.box.origin.x + self.box.size.x) + parallel
                        if height != self.building.heightmap[z][x] and dist < parallel:
                            dist = parallel
                            break

            output.append(dist)
        if direction == Direction.NONE or direction == Direction.SOUTH:
            dist = abs((self.box.origin.z + self.box.size.z) - (self.yard.origin.z + self.yard.size.z))
            if dist != 0:
                for perpendicular in range(self.box.size.x):
                    for parallel in range(dist):
                        z =
                        x = self.box.origin.x + perpendicular
                        if height != self.building.heightmap[z][x] and dist < parallel:
                            dist = parallel
                            break

            output.append(dist)
        if direction == Direction.NONE or direction == Direction.WEST:
            dist = abs((self.yard.origin.x) - (self.box.origin.x))
            if dist != 0:
                for perpendicular in range(self.box.size.z):
                    for parallel in range(dist):
                        if height != self.building.heightmap[offset.z - parallel][perpendicular + offsetx]:
                            dist = parallel
                            break

            output.append(dist)
        return output
