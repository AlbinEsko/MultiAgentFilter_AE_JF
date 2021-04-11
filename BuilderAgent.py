
from pymclevel import BoundingBox, MCLevel


def preform(level,box,options):
    print("preforming")


class BuilderAgent():

    def __init__(self, level, box):
        # type: (MCLevel, BoundingBox) -> None
        self.level =level
        self.box = box
        position = self.box.origin
        self.CreateHouses()

    def CreateHouses(self, nrModules):
        moduels = []
        for x in range(nrModules):
            print("s")




