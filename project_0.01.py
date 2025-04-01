import pygame
pygame.init()

screen=pygame.display.set_mode((800,600))
running=True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        pygame.display.set_caption("0.000000001")
    screen.fill((255,255,255))
    pygame.display.flip()

clock=pygame.time.Clock()
clock.tick(60)

#image=pygame.load("")  #dont have anything here
#screen.blit(image,(,))


pygame.draw.rect(screen(0,255,0),(50,50,100,100))
pygame.draw.circle(screen(255,0,0)(200,200),40)

class player:
    def __init__(self,x,y):
        self.width =40
        self.height=20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel=[0,0]
        self.speed= 5
        self.jump_power= -20
        self.gravity=1
        self.on_ground=False

    def handle_input(self,keys):
        if keys[pygame.K_LEFT]

pygame.quit()