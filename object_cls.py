from colour_cls import *
from vectors import Vector2

class Mass:
    def __init__(self, position: Vector2, velocity: Vector2, colour: Colour, mass: float, radius: float, field_strength: Vector2):
        self.pos = position
        self.vel = velocity
        self.colour = colour
        self.mass = mass
        self.radius = radius
        self.forces = Vector2.zero
        self.field_strength = field_strength
        self.freefalling = False

    def move(self, delta_time: float):
        self.pos = self.pos + self.vel * delta_time
        self.forces = Vector2.zero

    def accelerate(self, delta_time: float):
        self.vel = self.vel + self.forces * delta_time / self.mass
    
    @property
    def ke(self):
        return 0.5*self.mass*(self.vel.x**2+self.vel.y**2)

    @property
    def pe(self):
        return -self.mass*self.field_strength.dot(self.pos)
    
    @property
    def energy(self):
        return self.ke+self.pe

class FixedPoint:
    def __init__(self, position: Vector2):
        self.pos = position
        self.forces = Vector2.zero
        self.vel = Vector2.zero

class InelasticLightString:
    def __init__(self, start: FixedPoint | Mass, end: Mass, colour: Colour, real_length: float = -1):
        self.real_length = real_length
        if real_length == -1:
            self.real_length = (end.pos-start.pos).mag
        self.start = start
        self.end = end
        self.colour = colour
    
    @property
    def length(self):
        return (self.end.pos-self.start.pos).mag
    
    def pull(self, dt: float):
        _d1 = self.end.pos-self.start.pos+(self.end.vel-self.start.vel)*dt/2
        if _d1.mag >= self.real_length:
            if self.end.freefalling:
                self.end.freefalling = False
                return True
            # 
            _lambda = -((self.end.vel-self.start.vel)*(self.end.mass/dt)+self.end.forces).dot(_d1)/(self.real_length**2)#(_d1.x**2+_d1.y**2)
            if _lambda > 0:
                _lambda = 0
                self.end.freefalling = True
            self.end.forces += _d1*_lambda
            #print("\t",(_d1*_lambda).mag)
            if isinstance(self.start, Mass):
                self.start.forces -= _d1*_lambda
        else:
            self.end.freefalling = True
        return False
    
class Spring:
    def __init__(self, start: FixedPoint | Mass, end: Mass, colour: Colour, spring_constant: float, real_length: float = -1, default_width: float = 10):
        self.real_length = real_length
        if real_length == -1:
            self.real_length = (end.pos-start.pos).mag
        if real_length == -2:
            self.real_length = (end.pos-start.pos).mag-(end.mass*end.field_strength.mag/spring_constant)
        self.start = start
        self.end = end
        self.colour = colour
        self.spring_constant = spring_constant
        self.default_width = default_width
    
    @property
    def length(self):
        return (self.end.pos-self.start.pos).mag
    
    @property
    def epe(self):
        return 0.5*self.spring_constant*(self.length-self.real_length)**2
    
    @property
    def width(self):
        return self.default_width/max(self.length/self.real_length,1)
    
    def pull(self, dt: float):
        num = self.end.pos-self.start.pos+(self.end.vel-self.start.vel)*dt*0.5
        if num.mag >= self.real_length:
            if self.end.freefalling:
                self.end.freefalling = False
                return True
            force = -num.norm*(num.mag-self.real_length)*self.spring_constant
            self.end.forces += force
            self.start.forces -= force
        else:
            self.end.freefalling = True
        return False