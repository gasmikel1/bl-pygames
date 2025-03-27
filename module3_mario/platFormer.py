import pygame
import sys

pygame.init()

w=800
h=600

screen =pygame.display.set_mode((w,h))

clock=pygame.time.Clock()

pygame.display.set_caption("jumper")
platforms=[
    pygame.Rect(0,h-40,200,40),
    pygame.Rect(300,h-80,20,40),
    pygame.Rect(500,h-120,10,40),
    pygame.Rect(700,h-160,200,40),

]

running=True


while running:
    clock.tick(60)
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    for plat in platforms:
        pygame.draw.rect(screen,(0,255,0),(plat.w,plat.h, plat.x, plat.y))

    pygame.display.flip()