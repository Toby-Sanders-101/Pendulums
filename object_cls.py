from vectors import Vector2


# masses have position, velocity, mass, a gravitational field, kinetic energy, potential energy, and total energy
# for the drawing masses, they have a colour and a radius
# every frame their forces are summed to calculate the new velocity and position

class Mass:
    def __init__(self, position: Vector2, velocity: Vector2, colour: tuple, mass: float, radius: float, field_strength: Vector2):
        self.pos = position
        self.vel = velocity
        self.colour = colour
        self.mass = mass
        self.radius = radius
        self.forces = Vector2.zero
        self.field_strength = field_strength

    def experience_gravity(self):
        self.forces += self.field_strength * self.mass
    
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



# pivot points have position and velocity (given as functions over time)

class Point:
    def __init__(self, motion, velocity):
        self.motion = motion
        self.velocity = velocity
        self.forces = Vector2.zero
        self.time = 0
        self.reposition(0)

    def velocity(time) -> Vector2:
        pass
    
    def motion(time) -> Vector2:
        pass
    
    def reposition(self, dt):
        self.time += dt
        self.pos = self.motion(self.time)
        self.vel = self.velocity(self.time)



# this 'string' has a fixed length
# it is connected to a mass or point at each end

class String:
    def __init__(self, start: Point | Mass, end: Mass, colour: tuple, real_length: float = -1):
        self.real_length = real_length
        if real_length == -1:
            self.real_length = (end.pos-start.pos).mag
        self.start = start
        self.end = end
        self.colour = colour
    
    @property
    def length(self):
        return (self.end.pos-self.start.pos).mag
    
    # this is the function that ensures the length of the string is fixed
    def pull(self, dt: float):
        
        # find the displacement between the two ends of the string (half a frame in the future)
        s = self.end.pos-self.start.pos+(self.end.vel-self.start.vel)*dt/2
        
        # we want the relative velocity (relative to the other end) of the end point to be perpendicular to the displacement between the two ends
        # new relative velocity = relative velocity + forces*dt/mass
        # the tension/compression force ensures the total forces on the mass creates a new relative velocity that satisfies our condition
        # the tension/compression force acts parallel to the displacement between the two ends
        # change in velocity needed = (new relative velocity without the tension/compression force) dotted 
        #                                 with the direction of the displacement between the two ends
        # tension/compression force = mass*delta_v/dt in the direction of the displacement of the two ends
        delta_v = ((self.end.vel-self.start.vel)+(self.end.forces*dt/self.end.mass)).dot(s.norm)
        self.end.forces -= s.norm * delta_v*self.end.mass/dt
        
        # if the object at the other end is also a mass, pull on it
        if isinstance(self.start, Mass):
            self.start.forces += delta_v*self.end.mass/dt
