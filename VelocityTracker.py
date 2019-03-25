# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import math

class VelocityTracker():
    def __init__(self, objects):
        self.oldObjects = dict(objects)
        self.velocity = OrderedDict()
        self.objects = {}

    def update(self, newObjects):
        if len(self.objects) != 0:
            self.oldObjects = self.objects
        else:
            self.oldObjects = self.oldObjects
        
        self.objects = dict(newObjects)
        
    def velocityChange(self):
        for key in self.objects:
            if key in self.oldObjects:
                self.velocity[key] = math.sqrt(sum([(a - b) ** 2 for a, b in zip(self.objects[key], self.oldObjects[key])]))
            else:
                self.velocity[key] = 0
        self.oldObjects = self.objects
        return self.velocity    
            
if __name__ == '__main__':
    # first
    # centroidObject = OrderedDict()
    # centroidObject[1] = np.array((445, 143))
    # centroidObject[2] = np.array((123, 456))
    # vt = VelocityTracker(centroidObject)
    # print(vt.oldObjects)
    # centroidObject[2] = np.array((1, 2))
    # vt.update(centroidObject)
    # vt.velocityChange()
    # print(vt.velocity)
    centroidObject = OrderedDict()
    vt = VelocityTracker(centroidObject)
    print(vt.oldObjects)
    # print(centroidObject)
