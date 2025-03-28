import pygame
import sys

pygame.init()

w=800
h=600

class Player:
    def __init__(self,x,y):
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel = [0, 0]
        self.speed = 5
        self.jump_power = -15
        self.gravity = 1
        self.on_ground = False

    def handle_input(self,keys):
        if keys[pygame.K_LEFT]:
            self.vel[0] = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.vel[0] = self.speed
        else:
            self.vel[0] = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel[1] = self.jump_power
            self.on_ground = False
    
    def apply_physics(self,platforms):
        self.vel[1]+= self.gravity
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        self.on_ground = False
        for plat in platforms:
                if self.rect.colliderect(plat):
                    if self.vel[1] > 0 and self.rect.bottom <= plat.top + self.vel[1]:
                        self.rect.bottom = plat.top
                    self.vel[1] = 0
                self.on_ground = True 

def draw(self,surface,scroll_x):
  pygame.draw.rect(surface, (0,0,255), (self.rect.x - scroll_x, self.rect.y, self.width, self.height))


class Enemy:
    def __init__(self, x, y, w=40, h=40):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, (255,0,0), (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))

screen =pygame.display.set_mode((w,h))

clock=pygame.time.Clock()

pygame.display.set_caption("jumper")
platforms=[
    pygame.Rect(0,h-40,200,40),
    pygame.Rect(30,h-9,20,40),
    pygame.Rect(50,h-10,10,40),
    pygame.Rect(70,h-60,200,90),

]
player = Player(100, h - 150)
enemies = [Enemy(600, h - 100), Enemy(1100, h - 340)]

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
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.apply_physics(platforms)
    
    for enemy in enemies[:]:
        if player.rect.colliderect(enemy.rect):
            if player.vel[1] > 0 and player.rect.bottom <= enemy.rect.top + player.vel[1]:
                enemies.remove(enemy)
                player.vel[1] = player.jump_power // 2  # Bounce

    scroll_x = player.rect.x - w // 2

    # ============================
    # Step 12: Drawing
    # ============================
    for plat in platforms:
            pygame.draw.rect(screen, (0,255,0), (plat.x - scroll_x, plat.y, plat.w, plat.h))

    for enemy in enemies:
            enemy.draw(screen, scroll_x)

    player.draw(screen, scroll_x)                
    
    pygame.display.flip()