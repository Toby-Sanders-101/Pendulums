import pygame
from system_cls import *
import constants as const

pygame.init()

width, height = const.width, const.height

frame_rate = const.frame_rate
dt = 1/frame_rate
print(f"The simulation is running at {frame_rate}Hz")

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pendulum Simulation")

font = pygame.font.SysFont("comicsansms", 18)
small_font = pygame.font.SysFont("comicsansms", 14)

class Main:
    def __init__(self):
        self.cam = Camera(font, small_font, window)
        self.dt = dt
        self.running = True
        self.clock = pygame.time.Clock()
        offset = Vector2(const.width/2,const.height/4)

        self.objects = [
            #          pos,                  vel,           colour,      mass, radius, grav
            Mass(offset+Vector2(200,100), Vector2.zero, Colour(255,255,255), 10, 10, Vector2(0,400)),
            #Mass(offset+Vector2(100,0), Vector2.zero, Colour(255,  0,255), 1, 10, Vector2(0,400)),
            #Mass(offset+Vector2(200,100), Vector2.zero, Colour(0,255,255), 8, 10, Vector2(0,400)),
            #Mass(offset+Vector2(100,0), Vector2.zero, Colour(0,  0,255), 1, 10, Vector2(0,400))
            
            #Mass(offset+Vector2(0,283), Vector2(0,-65), Colour(255,255,255), 10, 10, Vector2(0,400))
        ]
        
        self.strings = [
            #                           start,           end,            colour,     real_length
            #InelasticLightString(self.objects[0], self.objects[1], Colour(255,255,255)),
            InelasticLightString(FixedPoint(offset), self.objects[0], Colour(255,255,255), 300),
            #InelasticLightString(self.objects[2], self.objects[3], Colour(255,255,255)),
            #InelasticLightString(FixedPoint(offset), self.objects[2], Colour(255,255,255), 300)
        ]

        self.springs = [
            #                start,           end,            colour,   spring constant, real_length, default_width
            #Spring(FixedPoint(offset), self.objects[0], Colour(255,255,255), 30, -2)
        ]
        
        print(f"Starting the simulation with {len(self.objects)} bodies")
        self.system = System3(self.objects, self.strings, self.springs, UniformGravitationalField(Vector2(0,400)), self.dt, self.cam)

    def start(self):
        while self.running:
            self.clock.tick(frame_rate)
            window.fill(const.background_colour)
            self.update()
            pygame.display.update()
        pygame.quit()

    def update(self):
        self.takeInputs()
        self.system.update_all()
    
    def takeInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


main = Main()
main.start()
