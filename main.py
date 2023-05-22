from td import *
import pygame
pygame.init()

width, height = 400, 400
sc = pygame.display.set_mode([width, height])
pygame.display.set_caption('3D Test')

frame = 0

c = FPSCamera(Vector3(-5, 0, 0), Vector3(0, 0, 0), 1, 0.05, aspect_ratio=width/height)
o1 = Cube(Vector3(1, 1, 1), 10, [(255, 0, 0), (255, 0, 0), (0, 255, 0), (0, 255, 0), (0, 0, 255), (0, 0, 255)])
o2 = Cube(Vector3(20, 1, 1), 5, [(255, 255, 0), (255, 255, 0), (0, 255, 255), (0, 255, 255), (255, 0, 255), (255, 0, 255)])
scene1 = Scene([o1, o2])


def update():
    sc.fill((0, 0, 0))
    scene1.render(sc, c)
    o1.rotate(Vector3(0.01, 0, 0.01))
    o2.move(Vector3(sin(PI/30 * frame), 0, 0))
    c.update(scene1)
    pygame.display.update()


clock = pygame.time.Clock()
while True:
    frame += 1
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    update()
