# import libraries and classes
import pygame
from object_cls import *
from data_window import *
import math

# create a pygame window and define some constants for later
pygame.init()
width, height = 1000, 800
background_colour = (0,0,0)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kapitza's Pendulum Simulation")

running = True
clock = pygame.time.Clock()

frame_rate = 240
dt = 1/frame_rate
print(f"The simulation is running at {frame_rate}Hz")

# define some constants. These can all be changed to vary the set up
offset = Vector2(500, 600)
g = 400
l = 400
mass = 10
radius = 10
A = 20 # << l
w = 40 # >> sqrt(g/l)
ydirection = Vector2(0,1)

# create functions that are the position and velocity over time of the pivot point
def oscillation_pos(time) -> Vector2:
    return offset+ydirection*A*math.sin(w*time)

def oscillation_vel(time) -> Vector2:
    return ydirection*A*w*math.cos(w*time)

# create lists of all the things. I have used lists so it can be extended to more objects 
objects = [Mass(offset+Vector2(80,-math.sqrt(l*l-6400)), Vector2.zero, (255,255,255), mass, radius, Vector2(0,g))]
points = [Point(oscillation_pos, oscillation_vel)]
strings = [String(points[0], objects[0], (255,255,255), l)]

# initialise the data window
datawindow = DataWindow(10, dt) # max 10 lines
datawindow.show()

# draw the strings and masses to the pygame window
def display():
    for line in strings:
        pygame.draw.line(window, line.colour, line.start.pos.tuple, line.end.pos.tuple)
    for mass in objects:
        pygame.draw.circle(window, mass.colour, mass.pos.tuple, mass.radius)

# sum all the forces on all the masses, then calculate their new positions, and find the new position of the pivot
def move_all():
    for body in objects:
        body.experience_gravity()
    for string in strings:
        string.pull(dt)
    for body in objects:
        body.accelerate(dt)
        body.move(dt)
    for point in points:
        point.reposition(dt)

# check that the user hasn't tried to close the window
def takeInputs():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# contiually calculate the new positions and update both the pygame and the data windows
while running:
    clock.tick(frame_rate)
    window.fill(background_colour)
    takeInputs()
    move_all()
    display()
    datawindow.update_plot_data(objects[0].ke, objects[0].pe+10*400*600, objects[0].energy+10*400*600)
    pygame.display.update()

pygame.quit()