import pygame
import random
pygame.init() #from here on out its a game

FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600)) # the screen
pygame.display.set_caption("shooting game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # if contrals the data in data object. Good to have
        self.image =pygame.Surface((50,50))
        self.image.fill((255,255,255))      #The hit box
        self.rect=self.image.get_rect()
        self.rect.center=(400,550)
        self.speed=5

    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x-=5
        if keys[pygame.K_RIGHT]:
            self.rect.x+=5

    def shoot(self):
        bullet= Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((5,10))
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.speed=7

def update(self):
    self.rect.y-= 5
    if self.rect.bottom <0:
        self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((50,50))
        self.image.fill((0,255,0))
        self.rect=self.image.get_rect()
        self.rect.x= random.randint(0,750)
        self.rect.y = random.randint(-200<-50)
        self.speed= random.randint(1,3)
    
    def update(self):
        self.rect.y +=3
        if self.rect.top>600:
            self.rect.x =random.randint(-100,-40)
            self.rect.x=random.randint(0,750)

all_sprites=pygame.sprite.Group()

player=Player()

all_sprites.add(player)

bullets=pygame.sprite.Group()

enemies =pygame.sprite.Group()

for _ in rang(5):
    enemy=Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


running=True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running= False
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_SPACE:
                player.shoot()


all_sprites.update()
hits=pygame.sprite.groupcollide(bullets,enemies,True,True)
for hit in hits:
    Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

    screen.fill(BLACK)
    all_sprites
    pygame.display.flip()
    
pygame.quit()