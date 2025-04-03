#mikels work
import pygame
pygame.init()
#
WIDTH, HEIGHT = 800, 600
#
screen=pygame.display.set_mode((WIDTH,HEIGHT))
#
running=True
#
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        pygame.display.set_caption("0.000000001")
    screen.fill((255,255,255))
    pygame.display.flip()

#==============================================
WHITE = (255, 255, 255)
BLUE = (66, 135, 245)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
#================================================
clock=pygame.time.Clock()
clock.tick(60)

#image=pygame.load("")  #dont have anything here
#screen.blit(image,(,))

#===================================================
#pygame.draw.rect(screen(0,255,0),(50,50,100,100))
#pygame.draw.circle(screen(255,0,0)(200,200),40)
#====================================================
class Player:
    def __init__(self,x,y):
        self.width =40
        self.height=20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel=[0,0]
        self.speed= 5
        self.jump_power= -20
        self.gravity=1
        self.on_ground=False
        self.speed = 7

#=========================================

scroll_x = Player.rect.x - WIDTH // 2
scroll_y = Player.rect.y - HEIGHT//2
#=================================================

class Enemy:
    def __init__(self, x, y, width=40, height=40):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, RED, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))
        enemies = [Enemy(600, HEIGHT - 100), Enemy(1100, HEIGHT - 340)]
#=====================================================
    def handle_input(self,keys):
            if keys[pygame.K_LEFT]:
                self.vel[0] = -self. speed
            elif keys[pygame.K_RIGHT]:
             self.vel[0] = +self. speed 
            else:
                self.vel[0] = 0
            if keys[pygame.K_SPACE] and self.on_ground:
                self.vel[1] = self. jump_power
                self.on_ground = False
            
#======================================================
    def apply_physics(self, platforms):
        self.vel[1] += self.gravity
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
#======================================================
    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, BLUE, (self.rect.x - scroll_x, self.rect.y, self.width, self.height))
#=====================================================
    def draw(self, surface, scroll_y):
        pygame.draw.rect(surface, BLUE, (self.rect.y - scroll_y, self.rect.y, self.width, self.height))
#======================================================
    platforms = [
    pygame.Rect(0, HEIGHT - 40, 2000, 40),
    pygame.Rect(300, HEIGHT - 150, 100, 20),
    pygame.Rect(500, HEIGHT - 250, 100, 20),
    pygame.Rect(750, HEIGHT - 180, 150, 20),
    pygame.Rect(1000, HEIGHT - 300, 100, 20),
    ]
#=======================================================
    player = Player(100, HEIGHT - 150)
#=======================================================
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

#=======================================================
    player.apply_physics(platforms)
    for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                if player.vel[1] > 0 and player.rect.bottom <= enemy.rect.top + player.vel[1]:
                    enemies.remove(enemy)
                    player.vel[1] = player.jump_power // 2  # Bounce
#==================================================
    for enemy in enemies:
            enemy.draw(screen, scroll_x)
#==================================================
    player.draw(screen, scroll_x)
    player.draw(screen,scroll_y)
#=================================================

pygame.quit()