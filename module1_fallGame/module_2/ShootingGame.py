import pygame

pygame.init() #from here on out its a game

screen = pygame.display.set_mode((800,600)) # the screen
pygame.display.set_caption("shooting game")

class Player():
    def __init__(self):
        super().__init__() # if contrals the data in data object. Good to have
        self.image =pygame.surface((50,50))
        self.image.fill((255,255,255))      #The hit box
        self.rect=self.image.get_rect()
        self.rect.center=(400,550)


running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running= False

pygame.quit()

