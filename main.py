from td import *
import pygame

width, height = 1600, 900
sc = pygame.display.set_mode([width, height])
pygame.display.set_caption('3D Test')

c = FPSCamera(Vector3(0, 0, 0), Vector3(0, 0, 0), 1, 0.05)
o1 = Cube(Vector3(1, 1, 1), 10, [(255, 0, 0), (255, 0, 0), (0, 255, 0), (0, 255, 0), (0, 0, 255), (0, 0, 255)])
o2 = Cube(Vector3(20, 1, 1), 5, [(255, 255, 0), (255, 255, 0), (0, 255, 255), (0, 255, 255), (255, 0, 255), (255, 0, 255)])
scene1 = Scene([o1, o2])


def update():
    sc.fill((255, 255, 255))
    scene1.render(sc, c)
    c.update()
    pygame.display.update()


clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    update()
