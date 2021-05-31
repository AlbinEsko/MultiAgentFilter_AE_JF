
from pymclevel import BoundingBox, MCLevel


def perform(level,box,options):
    print("preforming")


class BuilderAgent:

    def __init__(self, level, box):
        # type: (MCLevel, BoundingBox) -> None
        self.level = level
        self.box = box
        position = self.box.origin
        self.CreateHouse(box)
        self.buildings = []

    def CreateHouse(self,box):
        pass
