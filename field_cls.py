from vectors import *
from object_cls import *
from typing import List
from dataclasses import dataclass

class UniformGravitationalField:
    def __init__(self, acceleration_due_to_gravity: Vector2):
        self.g = acceleration_due_to_gravity

    def act_on(self, object: Mass):
        object.forces += self.g * object.mass

@dataclass
class FieldPair:
    centre: Vector2
    strength: float
    creator: Mass

class EField:
    def __init__(self):
        self.funcs: List[FieldPair] = []
    
    def inverse_square(self, fieldpair: FieldPair, object: Mass):
        r = object.pos - fieldpair.centre
        r_mag = r.mag
        r_norm = r.norm
        return r_norm * fieldpair.strength / r_mag**2
    
    def act_on(self, object: Mass):
        for func in self.funcs:
            if object is not func.creator:
                object.forces += self.inverse_square(func, object)