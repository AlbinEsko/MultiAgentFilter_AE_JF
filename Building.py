from pymclevel import BoundingBox, MCLevel
from collections import namedtuple
import random as random
from MAF_Utility import Direction
import utilityFunctions as uf

_expansion = namedtuple("_expansion", ("n", "e", "s", "w"))


class Building(object):
    def __init__(self, yard, level, heightmap):
        # type: (BoundingBox, MCLevel, List[List[int]]) -> None
        print("Building")
        self.yard = yard
        self.level = level
        self.heightmap = heightmap
        self.modules = []
        self.doors = []
        self.windows = []
        self.walls = []
        self.sizexmin = 5
        self.sizexmax = 10
        self.sizezmin = 5
        self.sizezmax = 10
        self.sizey = 5


class House(Building):
    def __init__(self, yard, level, heightmap):
        Building.__init__(self, yard, level, heightmap)

    def generate(self, nr_of_modules):
        # type: (int) -> House
        self.create_modules(nr_of_modules)
        self.create_walls()

    def create_modules(self, nr_of_modules):
        # type: (int) -> None
        ox = self.yard.origin.x + 1
        oz = self.yard.origin.z + 1
        oy = self.heightmap[1][1] + 1
        sx = 10
        sy = 15
        sz = 6
        box = BoundingBox([ox, oy, oz], [sx, sy, sz])
        module = Module(self.yard, box, self.level, self)
        print(box)
        self.modules.append(module)

        # for x in range(nr_of_modules):
        #     if x == 1:
        #         originx = random.randrange(0, 5)
        #         originz = random.randrange(0, 5)
        #     else:
        #         r = random.random()
        #         if r < 0.50:
        #             originx = self.modules[x - 1].size.x
        #             originz = random.randrange(0, 5)
        #         else:
        #             originx = random.randrange(0, 5)
        #             originz = self.modules[x - 1].size.z
        #
        #     originy = self.heightmap[originz][originx]  # this needs to be checked, might need to be inverted.
        #     origin = [originx, originy, originz]  # lowest x,y,z of box
        #     sizex = random.randrange(self.sizexmin, self.sizexmax)
        #     sizey = self.sizey
        #     sizez = random.randrange(self.sizezmin, self.sizezmax)
        #     size = [sizex, sizey, sizez]
        #     module = BoundingBox(origin, size)
        #     self.modules.append(BoundingBox)

    def create_walls(self):
        """For each module in building create wall for each side"""
        for module in self.modules:
            self.walls.append(self.create_north_wall(module))
            self.walls.append(self.create_east_wall(module))
            self.walls.append(self.create_south_wall(module))
            self.walls.append(self.create_west_wall(module))

        for wall in self.walls:
            self.fill_box(wall.box)
            self.create_pillars(wall)

    def create_north_wall(self, module):
        # type: (Module) -> BoundingBox
        m = module.box

        originx = module.box.origin.x
        originz = module.box.origin.z
        originy = module.box.origin.y
        sizex = module.box.size.x
        sizey = self.sizey
        sizez = 1
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.NORTH,self)
        return wall

    def create_east_wall(self, module):
        originx = module.box.origin.x + module.box.size.x - 1
        originz = module.box.origin.z
        originy = module.box.origin.y
        sizex = 1
        sizey = self.sizey
        sizez = module.box.size.z
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.EAST,self)
        return wall

    def create_south_wall(self, module):
        originx = module.box.origin.x
        originz = module.box.origin.z + module.box.size.z - 1
        originy = module.box.origin.y
        sizex = module.box.size.x
        sizey = self.sizey
        sizez = 1
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.SOUTH,self)
        return wall

    def create_west_wall(self, module):
        originx = module.box.origin.x
        originz = module.box.origin.z
        originy = module.box.origin.y
        sizex = 1
        sizey = self.sizey
        sizez = module.box.size.z
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.WEST,self)
        return wall

    def fill_box(self, box, block=5, blockid=0):
        # type: (BoundingBox) -> None

        xo = box.origin.x
        yo = box.origin.y
        zo = box.origin.z
        for y in range(box.size.y):
            for x in range(box.size.x):
                for z in range(box.size.z):
                    uf.setBlock(self.level, (block, blockid), xo + x, yo + y, zo + z)

    def create_pillars(self, wall, block=17, blockid=0):
        # type: (Wall, int, int) -> None
        """Creates cornerpillars of provided block"""

        x = wall.box.origin.x
        x1 = wall.box.origin.x + wall.box.size.x - 1
        # y = wall.origin.y
        ymax = wall.box.origin.y + wall.box.size.y
        z = wall.box.origin.z
        z1 = wall.box.origin.z + wall.box.size.z - 1
        for y in range(ymax):
            uf.setBlock(self.level, (block, blockid), x, y, z)
            uf.setBlock(self.level, (block, blockid), x1, y, z1)


class Module:
    """A module is a rectangle body of a building seen from above.
        ---------------
        |              |
        |              |
        |              |
        |              |
        |              |
        ---------------
    """

    def __init__(self, yard, box, level, building):
        # type: (BoundingBox, BoundingBox, MCLevel) -> None
        self.yard = yard
        self.box = box
        self.level = level
        self.building = building
        # self.expansion = self.getexpansionlimit(Direction.NONE)

    def getexpansionlimit(self, direction):
        # type: (Direction) -> [int]
        """Not working looking oustide of index in heightmap"""
        output = []
        offset = self.box.origin - self.yard.origin
        # offsetz = self.box.origin - self.yard.origin
        height = self.box.origin.y

        if direction == Direction.NONE or direction == Direction.NORTH:
            dist = abs(self.yard.origin.z - self.box.origin.z)
            if dist != 0:
                # perpendicular to direction
                for perpendicular in range(self.box.size.x):
                    for parallel in range(dist):
                        z = (self.box.origin.z - 1) - parallel
                        x = self.box.origin.x + perpendicular
                        print(z, x)
                        if height != self.building.heightmap[z][x] and dist < parallel:
                            dist = parallel
                            break
            output.append(dist)

        if direction == Direction.NONE or direction == Direction.EAST:
            dist = abs((self.yard.origin.x + self.yard.size.x) - (self.box.origin.x + self.box.size.x))
            if dist != 0:
                for perpendicular in range(self.box.size.z):
                    for parallel in range(dist):
                        z = self.origin.z + perpendicular
                        x = (self.box.origin.x + self.box.size.x + 1) + parallel
                        if height != self.building.heightmap[z][x] and dist < parallel:
                            dist = parallel
                            break

            output.append(dist)

        if direction == Direction.NONE or direction == Direction.SOUTH:
            dist = abs((self.box.origin.z + self.box.size.z) - (self.yard.origin.z + self.yard.size.z))
            if dist != 0:
                for perpendicular in range(self.box.size.x):
                    for parallel in range(dist):
                        z = (self.box.origin.z + self.box.size.z + 1) + parallel
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
                        z = self.origin.z + perpendicular
                        x = (self.box.origin.x + self.box.size.x - 1) - parallel
                        if height != self.building.heightmap[z][x] and dist < parallel:
                            dist = parallel
                            break

            output.append(dist)

        return output


class Wall:

    def __init__(self, box, direction, building):
        # type: (BoundingBox, Direction) -> None
        self.box = box
        self.window = []
        self.door = []
        self.direction = direction
        self.building = building

    def build_door(self):
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            middle = self.box.o
