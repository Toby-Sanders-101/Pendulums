import numpy as np
from typing import Self

# this defines the operations for 2d vectors so you can add/subtract them, 
# multiply/divide by a scalar, or take the dot product of them.
# you can get the length of a vector, or get the normalised vector

class Vector2:
    zero: Self = None
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, b: Self) -> Self:
        return Vector2(self.x+b.x, self.y+b.y)
    
    def __sub__(self, b: Self) -> Self:
        return Vector2(self.x-b.x, self.y-b.y)
    
    def __mul__(self, k: float) -> Self:
        return Vector2(self.x * k, self.y * k)
    
    def __truediv__(self, k: float) -> Self:
        if k == 0:
            return Vector2.zero
        return Vector2(self.x / k, self.y / k)
    
    def __neg__(self) -> Self:
        return Vector2(-self.x, -self.y)
    
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def dot(self, b: Self) -> float:
        return self.x * b.x + self.y * b.y

    @property
    def mag(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)

    @property
    def norm(self) -> Self:
        return self / self.mag
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y)

Vector2.zero = Vector2(0,0)