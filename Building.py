from pymclevel import BoundingBox, MCLevel
from collections import namedtuple
import random as random
from MAF_Utility import Direction
import utilityFunctions as uf
from pymclevel.box import Vector
import Furniture as fur
import FurnitureAgent as furagent




class Building(object):
    def __init__(self, box, yard, level, heightmap, dir_to_road):
        # type: (BoundingBox, MCLevel, List[List[int]], Direction) -> None
        print("Building")
        self.box = box
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
        self.sizexmin = 6
        self.sizexmax = 12
        self.sizezmin = 6
        self.sizezmax = 12
        self.sizey = 5


def randomalowed(lower, max, limit):
    r = random.randrange(lower,max)
    if r > limit:
        r = limit
    return r


class House(Building):
    def __init__(self, box, yard, level, heightmap, dir_to_road):
        Building.__init__(self, box, yard, level, heightmap, dir_to_road)

    def generate(self):
        # type: (int) -> House
        self.create_modules()
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
                         # print("free slot" + str(free_slots))
                        wall.build_door(random.choice(free_slots))
                        doors_available -= 1

        for module in range(len(self.modules)):
            for wall in self.walls[module * 4:module * 4 + 4]:
                tries = 5
                while wall.resources > 0 and tries > 0:
                    free_slots = self.get_free_slots(wall.slots)
                    if len(free_slots) == 0:
                        break
                    if not wall.build_window(random.choice(free_slots), random.randint(2, 4)):
                        tries -= 1

        self.create_floorplan()
        # self.printfloorplans()
        self.populatefloorplans()
        agent = furagent.FurnitureAgent(self.floorplans)
        agent.Act()
        self.buildfloorplans()
        self.printfloorplans()






        # for wall in self.walls:
        #     print(wall.slots)

    def printfloorplans(self):
        print("Floorplan:")
        for plan in self.floorplans:
            print("length" + str(len(self.floorplans)))
            for i in plan:
                print(i)

    def create_modules(self):
        # type: (int) -> None
        # print()
        # print()
        # print("values")
        # print(self.sizexmin)
        # print(self.sizexmax)
        # print(self.yard.size.x)

        # sx = random.randrange(6,12)
        sx = randomalowed(self.sizexmin,self.sizexmax,self.yard.size.x)
        # sx = 10
        sy = self.sizey
        sz =randomalowed(self.sizezmin,self.sizezmax,self.yard.size.z)
        # sz = 6
        # print("values")
        # print("sx = " + str(sx))
        # print("sz = " + str(sz))

        x = self.yard.size.x - sx
        z = self.yard.size.z - sz

        ox = self.yard.origin.x + random.randrange(0,x)
        oz = self.yard.origin.z + random.randrange(0,z)
        oy = self.heightmap[oz - self.box.origin.z][ox - self.box.origin.x] + 1



        box = BoundingBox([ox, oy, oz], [sx, sy, sz])
        module = Module(self.yard, box, self.level, self)
        # print(box)
        self.fill_box(BoundingBox(box,[sx,20,sz]),0) # clearing from wood and leaves
        self.modules.append(module)

        self.modules.append(module.addfloor())

        # r = random.random()
        # if r < 0.3 and self.sizexmin >= 6 and self.sizezmin >=6:
        #     self.modules.append(module.addfloor())


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

            # floorplan[2][5] = "CW"
            counter += 1
            self.floorplans.append(floorplan)



    def getsymbol(self, param):
        "returns corresponding symbol to the floorplan"
        if param == None:
            return "W"

        return param

    def populatefloorplans(self):

        if len(self.modules) >1:
            self.placestairs(self.floorplans, self.walls[0:4])

        pass

    def buildfloorplans(self):
        # print("Building floorplans")
        module = 0
        for plan in self.floorplans:
            for z in range(len(plan)):
                # print(plan[z])
                for x in range(len(plan[z])):
                    self.buildfurniture(self.modules[module],plan[z-1][x-1],x,z)
            module += 1

    def buildfurniture(self, module, furniture, x, z):
        # print("Building furniture :" + str(furniture))

        xo = module.box.origin.x - 1 +x
        zo = module.box.origin.z - 1 +z
        y = module.box.origin.y
        if furniture == "S":  # bookShelf
            fur.Bookshelf(self.level, xo, y, zo)
        elif furniture[0] == "B":
            dir = self.getrotationint(furniture[1])
            fur.Bed(self.level, xo, y, zo, dir)
        elif furniture[0:2] =="ST":  # Stairs
            dir = self.getrotationint(furniture[2])
            height = int(furniture[3])
            fur.Stair(self.level,xo,y,zo,dir,height)
        elif furniture == "FN": #Fence
            fur.Fence(self.level,xo,y,zo)
        elif furniture[0] == "F":  # Furnace
            dir = self.getrotationint(furniture[1])
            fur.Furnace(self.level,xo,y,zo,dir)
        elif furniture[0:2] == "CO":  # Corner
            fur.Corner(self.level,xo,y,zo, furniture[2])
        elif furniture[0] == "C":  # Chest
            dir = self.getrotationint(furniture[1])
            fur.Chest(self.level,xo,y,zo,dir)



    def getrotationint(self,char):
        if char == "N":
            return 1
        elif char == "E":
            return 2
        elif char == "S":
            return 3
        elif char == "W":
            return 4
        return 0

    def placestairs(self,floorplan,walls):

        s = Stairs(floorplan[0],walls)
        stairs = s.getrandomstairs()
        counter = 0
        for coord in stairs:
            floorplan[0][coord.z][coord.x] = coord.container
            if counter >0:
                floorplan[1][coord.z][coord.x] = "N"
            counter+=1

        last = stairs[-1]
        floorplan[1][last.z][last.x] = "E"





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
        self.door.append(slot)
        # self.resources -= 1

    def build_window(self, slot, width, height=2, block=20):
        """Builds window, default Glass block"""
        for x in range(width):
            try:
                if self.slots[slot + x] is not None:
                    # print("Trying to build on already build slot, exiting")
                    return False
            except IndexError:
                # print("Trying outside of slots")
                return False
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
        return True

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
    def containsdoor(self):
        if len(self.door) > 0:
            return True
        return False


class Stairs:
    def __init__(self, floorplan, walls):
        self.floorplan = floorplan
        self.available_stairs = []
        self.createstairs(walls)




    def createstairs(self, walls):
        # type: (None,Module) -> None
        for wall in range(len(walls)):
            # print(walls[wall].slots)
            print("This wall contains a door: "+ str(walls[wall].containsdoor()))
            if walls[wall].containsdoor():
                # print("Stairs left before " + str(len(self.available_stairs)))
                w = walls[wall]
                length = len(walls[wall].slots)
                slot = w.door[0]
                # print()
                print("slot is: " + str(slot) + " Lenght is: " + str(length))
                if slot <= 1 or slot >= length-1 or length <= 5:
                    # print("Removing incompatible stairs")
                    if wall == 0:
                        self.addcornerstairs("SE")
                        self.addcornerstairs("SW")
                    elif wall == 1:
                        print("Removing incompatible stairs")
                        self.addcornerstairs("NW")
                        self.addcornerstairs("SW")
                    elif wall == 2:
                        self.addcornerstairs("NW")
                        self.addcornerstairs("NE")
                    elif wall == 3:
                        self.addcornerstairs("NE")
                        self.addcornerstairs("SE")
                else:
                    self.addcornerstairs("NW")
                    self.addcornerstairs("NE")
                    self.addcornerstairs("SE")
                    self.addcornerstairs("SW")

                # print("Wall " + str(wall) + " contains a door")
                # print("Stairs left after " + str(len(self.available_stairs)))


    def addcornerstairs(self,allowed_corners):
        if "NW" in allowed_corners:
            temp= [Coordinate(1,3),
                   Coordinate(1,2),
                   Coordinate(1,1),
                   Coordinate(2,1),
                   Coordinate(3,1),
                   Coordinate(4,1)]
            forward = []
            forward.extend([temp[0].setcontainer("STN0"),
                           temp[1].setcontainer("STN1"),
                           temp[2].setcontainer("CO2"),
                           temp[3].setcontainer("STE2"),
                           temp[4].setcontainer("STE3"),
                           temp[5].setcontainer("STE4")])
            backward = []
            backward.extend([temp[5].setcontainer("STW0"),
                           temp[4].setcontainer("STW1"),
                           temp[3].setcontainer("STW2"),
                           temp[2].setcontainer("CO3"),
                           temp[1].setcontainer("STS3"),
                           temp[0].setcontainer("STS4")])
            self.available_stairs.append(forward)
            self.available_stairs.append(backward)
        if "NE" in allowed_corners:
            x = len(self.floorplan[0])-2
            temp = [Coordinate(x-2,1),
                    Coordinate(x-1, 1),
                    Coordinate(x, 1),
                    Coordinate(x, 2),
                    Coordinate(x, 3),
                    Coordinate(x, 4)]
            forward = []
            forward.extend([temp[0].setcontainer("STE0"),
                            temp[1].setcontainer("STE1"),
                            temp[2].setcontainer("CO2"),
                            temp[3].setcontainer("STS2"),
                            temp[4].setcontainer("STS3"),
                            temp[5].setcontainer("STS4")])
            backward = []
            backward.extend([temp[5].setcontainer("STN0"),
                             temp[4].setcontainer("STN1"),
                             temp[3].setcontainer("STN2"),
                             temp[2].setcontainer("CO3"),
                             temp[1].setcontainer("STW3"),
                             temp[0].setcontainer("STW4")])
            self.available_stairs.append(forward)
            self.available_stairs.append(backward)
        if "SE" in allowed_corners:
            x = len(self.floorplan[0]) - 2
            z = len(self.floorplan) - 2
            temp = [Coordinate(x, z-2),
                    Coordinate(x, z-1),
                    Coordinate(x, z),
                    Coordinate(x-1, z),
                    Coordinate(x-2, z),
                    Coordinate(x-3, z)]
            forward = []
            forward.extend([temp[0].setcontainer("STS0"),
                            temp[1].setcontainer("STS1"),
                            temp[2].setcontainer("CO2"),
                            temp[3].setcontainer("STW2"),
                            temp[4].setcontainer("STW3"),
                            temp[5].setcontainer("STW4")])
            backward = []
            backward.extend([temp[5].setcontainer("STE0"),
                             temp[4].setcontainer("STE1"),
                             temp[3].setcontainer("STE2"),
                             temp[2].setcontainer("CO3"),
                             temp[1].setcontainer("STN3"),
                             temp[0].setcontainer("STN4")])
            self.available_stairs.append(forward)
            self.available_stairs.append(backward)
        if "SW" in allowed_corners:
            z = len(self.floorplan) - 2
            temp = [Coordinate(3, z),
                    Coordinate(2, z),
                    Coordinate(1, z),
                    Coordinate(1, z-1),
                    Coordinate(1, z-2),
                    Coordinate(1, z-3)]
            forward = []
            forward.extend([temp[0].setcontainer("STW0"),
                            temp[1].setcontainer("STW1"),
                            temp[2].setcontainer("CO2"),
                            temp[3].setcontainer("STN2"),
                            temp[4].setcontainer("STN3"),
                            temp[5].setcontainer("STN4")])
            backward = []
            backward.extend([temp[5].setcontainer("STS0"),
                             temp[4].setcontainer("STS1"),
                             temp[3].setcontainer("STS2"),
                             temp[2].setcontainer("CO3"),
                             temp[1].setcontainer("STE3"),
                             temp[0].setcontainer("STE4")])
            self.available_stairs.append(forward)
            self.available_stairs.append(backward)


    def getrandomstairs(self):
        r = random.randrange(0,len(self.available_stairs))
        # print("Chosen stair" + str(r))
        return self.available_stairs[r]

class Coordinate:
    def __init__(self,x,z,container = None):
        self.x = x
        self.z = z
        self.container = container


    def setcontainer(self,container):
        self.container = container

        return Coordinate(self.x,self.z,container)
