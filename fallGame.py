#This is Mikel's Work 


import pygame # use this to make game
import random # use this to make random falling objects
# set up game window
pygame.init() # need this, this is step one every thing after this is a game 


height=600
width=800
WHITE=(255,255,255)
screen=pygame.display.set_mode((width,height)) # makes a screen
pygame.display.set_caption("falling stuff") 

clock= pygame.time.Clock() #games run on frames

FPS= 60 # game updates 60 times every second
running=True

# step 2. make user character object
# a object is a construct that holds both functions and data that 
#represent speific thing

class Player:# class 
    def _init_(self):
        self.x = width // 2 #Start in middle
        self.y = height - 60 # near the bottom
        self.PlayerWidth= 50
        self.playerHight= 50
        self.playerSpeed= 5 #speed

    def move(self,keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x-=self.playerSpeed
        if keys[pygame.K_RIGHT] and self.x <width - self.PlayerWidth:
            self.x += self.playerSpeed 
   
    def draw(self):
        pygame.draw.rect(screen, (0, 0, 255),
        (self.x, self.y,self.PlayerWidth ,self.playerHight))

class FallingObject:
    def _init_(self):
        self.x= random.randint(0,width-50)
        self.y=-50
        self.width=50
        self.height= 50
        self.speed= random.randint(1,9)

    def move(self):
        self.y +=self.speed

    def draw(self):
        pygame.draw.rect(screen, (255,0,0),(self.x,self.y,self.width,self.height))

def off_screen(self):
    return self.y >height


player=Player()
falling_object =[]
score = 0
lives =3


while running: 
    clock.tick(FPS)
    screen.fill(WHITE)
    
    keys=pygame.key.get_pressed()
    player.move(keys)
    player.draw()

     #makes the game run like really thats this
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #clock.tick(FPS)

pygame.quit()

