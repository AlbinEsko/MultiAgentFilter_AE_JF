from pymclevel import BoundingBox, MCLevel
from collections import namedtuple
import random as random
from MAF_Utility import Direction
import utilityFunctions as uf
from pymclevel.box import Vector
import Furniture as fur

_expansion = namedtuple("_expansion", ("n", "e", "s", "w"))


class Building(object):
    def __init__(self, yard, level, heightmap, dir_to_road):
        # type: (BoundingBox, MCLevel, List[List[int]], Direction) -> None
        print("Building")
        self.yard = yard
        self.level = level
        self.heightmap = heightmap
        self.dir_to_road = dir_to_road
        self.modules = []
        self.floor = []
        self.doors = []
        self.windows = []
        self.walls = []
        self.floorplans = []
        self.sizexmin = 5
        self.sizexmax = 10
        self.sizezmin = 5
        self.sizezmax = 10
        self.sizey = 5


class House(Building):
    def __init__(self, yard, level, heightmap, dir_to_road):
        Building.__init__(self, yard, level, heightmap, dir_to_road)

    def generate(self, nr_of_modules):
        # type: (int) -> House
        self.create_modules(nr_of_modules)
        self.create_floor()
        self.create_walls()

        total_doors = 0
        for module in self.modules:
            if module.isgroundfloor:
                total_doors += 1
        # total_doors = len(self.modules)
        # print("Total doors: " + str(total_doors))
        for module in range(len(self.modules)):
            if self.modules[module].istoplevel:
                self.build_roof(self.modules[module])

        doors_available = 0
        for module in range(len(self.modules)):
            if total_doors > 0:
                doors_available = 1
                total_doors -= 1

            for wall in self.walls[module * 4:module * 4 + 4]:
                if doors_available > 0:
                    if wall.wall_side.value is self.dir_to_road.value:
                        free_slots = self.get_free_slots(wall.slots)
                        print("free slot" + str(free_slots))
                        wall.build_door(random.choice(free_slots))
                        doors_available -= 1

        for module in range(len(self.modules)):
            for wall in self.walls[module * 4:module * 4 + 4]:
                while wall.resources > 0:
                    free_slots = self.get_free_slots(wall.slots)
                    if len(free_slots) == 0:
                        break
                    wall.build_window(random.choice(free_slots), random.randint(2, 4))

        self.create_floorplan()
        self.printfloorplans()
        self.populatefloorplans()
        self.buildfloorplans()

        for wall in self.walls:
            print(wall.slots)

    def printfloorplans(self):
        print("Floorplan:")
        for plan in self.floorplans:
            print("length" + str(len(self.floorplans)))
            for i in plan:
                print(i)

    def create_modules(self, nr_of_modules):
        # type: (int) -> None
        ox = self.yard.origin.x + 1
        oz = self.yard.origin.z + 1
        oy = self.heightmap[1][1] + 1
        # print( "oy" + str(oy))
        sx = 10
        sy = self.sizey
        sz = 7
        box = BoundingBox([ox, oy, oz], [sx, sy, sz])
        module = Module(self.yard, box, self.level, self)
        print(box)
        self.modules.append(module)
        self.modules.append(module.addfloor())

        # r = random.random()
        # if r < 0.3:
        #     self.modules.append(module.addfloor())

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
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.NORTH, self)
        return wall

    def create_east_wall(self, module):
        originx = module.box.origin.x + module.box.size.x - 1
        originz = module.box.origin.z
        originy = module.box.origin.y
        sizex = 1
        sizey = self.sizey
        sizez = module.box.size.z
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.EAST, self)
        return wall

    def create_south_wall(self, module):
        originx = module.box.origin.x
        originz = module.box.origin.z + module.box.size.z - 1
        originy = module.box.origin.y
        sizex = module.box.size.x
        sizey = self.sizey
        sizez = 1
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.SOUTH, self)
        return wall

    def create_west_wall(self, module):
        originx = module.box.origin.x
        originz = module.box.origin.z
        originy = module.box.origin.y
        sizex = 1
        sizey = self.sizey
        sizez = module.box.size.z
        wall = Wall(BoundingBox([originx, originy, originz], [sizex, sizey, sizez]), Direction.WEST, self)
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
        y = wall.box.origin.y
        ymax = + wall.box.size.y
        # print(wall.box.origin.y, wall.box.size.y)
        z = wall.box.origin.z
        z1 = wall.box.origin.z + wall.box.size.z - 1
        for i in range(ymax):
            uf.setBlock(self.level, (block, blockid), x, y + i, z)
            uf.setBlock(self.level, (block, blockid), x1, y + i, z1)

    def get_free_slots(self, slots):
        # type: ([]) -> [int]
        free_slots = []
        for x in range(len(slots)):
            if slots[x] == None:
                free_slots.append(x)
        return free_slots

    def create_floor(self):
        for module in self.modules:
            origin = Vector(module.box.origin.x, module.box.origin.y - 1, module.box.origin.z)
            size = Vector(module.box.size.x, 1, module.box.size.z)
            floor = BoundingBox(origin, size)
            self.floor.append(floor)
            self.fill_box(floor)

    def build_roof(self, module, block=53):
        # type: (Module) -> None
        big_dir = module.getbiggestdimension()
        xsize = module.box.size.x
        zsize = module.box.size.z
        xpos = module.box.origin.x
        zpos = module.box.origin.z
        ypos = module.box.origin.y + module.box.size.y

        if big_dir == "x":
            if zsize % 2 == 1:  # if uneven
                self.build_roof_uneven(block, xpos, xsize, ypos, zpos, zsize, big_dir)
            else:  # if even
                self.build_roof_even(block, xpos, xsize, ypos, zpos, zsize, big_dir)
        else:
            if xsize % 2 == 1:  # if uneven
                self.build_roof_uneven(block, xpos, xsize, ypos, zpos, zsize, big_dir)
            else:  # if even
                self.build_roof_even(block, xpos, xsize, ypos, zpos, zsize, big_dir)

    def build_roof_even(self, block, xpos, xsize, ypos, zpos, zsize, big_dir):
        if big_dir == "x":
            blockidNorth = 2
            blockidSouth = 3
            for z in range(zsize / 2):

                for x in range(xsize):
                    uf.setBlock(self.level, (block, blockidNorth), xpos + x, ypos + z, zpos + z)
                    uf.setBlock(self.level, (block, blockidSouth), xpos + x, ypos + z, zpos + zsize - z - 1)

                if z > 1:
                    for z1 in range(z + 1):
                        for y1 in range(z1):
                            # print("z = "+ str(z) + "z1 = " + str(z1))
                            uf.setBlock(self.level, (5, 0), xpos, ypos + y1, zpos + z1)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - 1, ypos + y1, zpos + z1)
                            uf.setBlock(self.level, (5, 0), xpos, ypos + y1, zpos + zsize - z1 - 1)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - 1, ypos + y1, zpos + zsize - z1 - 1)
        else:
            blockidEast = 0
            blockidWest = 1
            for x in range(xsize / 2):

                for z in range(zsize):
                    uf.setBlock(self.level, (block, blockidEast), xpos + x, ypos + x, zpos + z)
                    uf.setBlock(self.level, (block, blockidWest), xpos + xsize - x - 1, ypos + x, zpos + z)

                if x > 1:
                    for x1 in range(x + 1):
                        for y1 in range(x1):
                            # print("z = "+ str(z) + "z1 = " + str(z1))
                            uf.setBlock(self.level, (5, 0), xpos + x1, ypos + y1, zpos)
                            uf.setBlock(self.level, (5, 0), xpos + x1, ypos + y1, zpos + zsize - 1)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - x1 - 1, ypos + y1, zpos)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - x1 - 1, ypos + y1, zpos + zsize - 1)

    def build_roof_uneven(self, block, xpos, xsize, ypos, zpos, zsize, big_dir):
        if big_dir == "x":
            blockidNorth = 2
            blockidSouth = 3
            for z in range(zsize - 1):

                for x in range(xsize):
                    uf.setBlock(self.level, (block, blockidNorth), xpos + x, ypos + z, zpos + z)
                    uf.setBlock(self.level, (block, blockidSouth), xpos + x, ypos + z, zpos + zsize - z - 1)

                if z > 1:
                    for z1 in range(z + 1):
                        for y1 in range(z1):
                            # print("z = "+ str(z) + "z1 = " + str(z1))
                            uf.setBlock(self.level, (5, 0), xpos, ypos + y1, zpos + z1)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - 1, ypos + y1, zpos + z1)
                            uf.setBlock(self.level, (5, 0), xpos, ypos + y1, zpos + zsize - z1 - 1)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - 1, ypos + y1, zpos + zsize - z1 - 1)
                if z == ((zsize / 2) - 1):
                    for x in range(xsize):
                        for y1 in range(zsize / 2 + 1):
                            if x == 0 or x == xsize - 1:
                                uf.setBlock(self.level, (5, 0), xpos + x, ypos + y1 - 1, zpos + z + 1)
                            uf.setBlock(self.level, (5, 0), xpos + x, ypos + zsize / 2 - 1, zpos + z + 1)
                    break
        else:
            blockidEast = 0
            blockidWest = 1
            # print("xsize - 1 = " + str(xsize - 1))
            # print("zsize = " + str(zsize))
            for x in range(xsize - 1):

                for z in range(zsize):
                    uf.setBlock(self.level, (block, blockidEast), xpos + x, ypos + x, zpos + z)
                    uf.setBlock(self.level, (block, blockidWest), xpos + xsize - x - 1, ypos + x, zpos + z)

                if x > 1:
                    for x1 in range(x + 1):
                        for y1 in range(x1):
                            # print("z = "+ str(z) + "z1 = " + str(z1))
                            uf.setBlock(self.level, (5, 0), xpos + x1, ypos + y1, zpos)
                            uf.setBlock(self.level, (5, 0), xpos + x1, ypos + y1, zpos + zsize - 1)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - x1 - 1, ypos + y1, zpos)
                            uf.setBlock(self.level, (5, 0), xpos + xsize - x1 - 1, ypos + y1, zpos + zsize - 1)
                if x == ((xsize / 2) - 1):
                    for z in range(zsize):
                        for y1 in range(xsize / 2 + 1):
                            if z == 0 or z == zsize - 1:
                                uf.setBlock(self.level, (5, 0), xpos + x + 1, ypos + y1 - 1, zpos + z)
                        uf.setBlock(self.level, (5, 0), xpos + x + 1, ypos + xsize / 2 - 1, zpos + z)
                    break

    def create_floorplan(self):
        counter = 0
        for module in self.modules:
            floorplan = [["0" for i in range(module.box.size.x)] for j in range(module.box.size.z)]
            for wall in self.walls[counter * 4:counter * 4 + 4]:
                if wall.wall_side == Direction.NORTH:  # north wall
                    floorplan[0][0] = "W"
                    floorplan[0][len(floorplan[0]) - 1] = "W"
                    for x in range(len(wall.slots)):
                        floorplan[0][x + 1] = self.getsymbol(wall.slots[x])
                elif wall.wall_side == Direction.EAST:  # east wall
                    for z in range(len(wall.slots)):
                        floorplan[z + 1][len(floorplan[0]) - 1] = self.getsymbol(wall.slots[z])
                elif wall.wall_side == Direction.SOUTH:  # east wall
                    floorplan[len(floorplan)-1][0] = "W"
                    floorplan[len(floorplan)-1][len(floorplan[0]) - 1] = "W"
                    for x in range(len(wall.slots)):
                        floorplan[len(floorplan)-1][x+1] = self.getsymbol(wall.slots[x])
                elif wall.wall_side == Direction.WEST:
                    for z in range(len(wall.slots)):
                        floorplan[z + 1][0] = self.getsymbol(wall.slots[z])

            floorplan[1][1] = "S"
            counter += 1
            self.floorplans.append(floorplan)



    def getsymbol(self, param):
        "returns corresponding symbol to the floorplan"
        if param == None:
            return "W"

        return param

    def populatefloorplans(self):
        pass

    def buildfloorplans(self):
        print("Building floorplans")
        module = 0
        for plan in self.floorplans:
            for z in range(len(plan)):
                print(plan[z])
                for x in range(len(plan[z])):
                    self.buildfurniture(self.modules[module],plan[z-1][x-1],x,z)
            module += 1

    def buildfurniture(self, module, furniture, x, z):
        print("Building furniture :" +str(furniture))
        xo = module.box.origin.x -1
        zo = module.box.origin.z -1
        if furniture == "S":
            fur.Bookshelf(self.level,xo+x,module.box.origin.y,zo+z)



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
        self.istoplevel = True
        self.isgroundfloor = True
        # self.expansion = self.getexpansionlimit(Direction.NONE)

    def getexpansionlimit(self, direction):
        # type: (Direction) -> [int]
        """Not working looking outside of index in heightmap"""
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

    def getbiggestdimension(self):
        """Returns whether the x or z axis are the biggest"""
        if self.box.size.x > self.box.size.z:
            return "x"
        else:
            return "z"

    def addfloor(self):
        # Type: (Module) -> Module
        self.istoplevel = False
        neworigin = [self.box.origin.x, self.box.origin.y + self.box.size.y, self.box.origin.z]
        newbox = BoundingBox(neworigin, self.box.size)
        newfloor = Module(self.yard, newbox, self.level, self.building)
        newfloor.isgroundfloor = False
        return newfloor


class Wall:

    def __init__(self, box, wall_side, building):
        # type: (BoundingBox, Direction) -> None
        self.box = box
        self.window = []
        self.door = []
        self.wall_side = wall_side
        self.building = building
        self.slots = [None] * (self.get_length() - 2)
        self.resources = len(self.slots) / 3

    def build_door(self, slot, block=64, ):
        """Builds door, default oakdoor"""
        data1 = 9  # Upper, Right Hinge, Unpowered
        data2 = self.get_rotation_door_data()
        x = 0
        y = self.box.origin.y + 1
        z = 0

        if self.wall_side == Direction.NORTH or self.wall_side == Direction.SOUTH:
            x = self.box.origin.x + slot + 1
            z = self.box.origin.z
        else:
            x = self.box.origin.x
            z = self.box.origin.z + slot + 1
        uf.setBlock(self.building.level, (block, data1), x, y, z)
        uf.setBlock(self.building.level, (block, data2), x, y - 1, z)
        self.slots[slot] = "D"
        # self.resources -= 1

    def build_window(self, slot, width, height=2, block=20):
        """Builds window, default Glass block"""
        for x in range(width):
            try:
                if self.slots[slot + x] is not None:
                    # print("Trying to build on already build slot, exiting")
                    return
            except IndexError:
                # print("Trying outside of slots")
                return
        y = self.box.origin.y + height
        x_forward = True
        if self.wall_side == Direction.NORTH or self.wall_side == Direction.SOUTH:
            x = self.box.origin.x + slot + 1
            z = self.box.origin.z
        else:
            x_forward = False
            x = self.box.origin.x
            z = self.box.origin.z + slot + 1

        for i in range(width):
            self.slots[slot + i] = "G"
            for j in range(height):
                if x_forward:
                    uf.setBlock(self.building.level, (block, 0), x + i, y - j, z)
                else:
                    uf.setBlock(self.building.level, (block, 0), x, y - j, z + i)

        self.resources -= 1

    def get_length(self):
        """Returns the length of the wall"""
        if self.wall_side == Direction.NORTH or self.wall_side == Direction.SOUTH:
            return self.box.size.x
        return self.box.size.z

    def get_rotation_door_data(self):
        if self.wall_side == Direction.NORTH:
            return 1
        elif self.wall_side == Direction.EAST:
            return 2
        elif self.wall_side == Direction.SOUTH:
            return 3
        else:  # self.wall_side == Direction.WEST:
            return 0
