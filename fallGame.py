#This is Mikel's work, MY WORK! 


import pygame # use this to make game
import random # use this to make random falling objects
# set up game window
pygame.init() # need this, this is step one every thing after this is a game 


height=1000
width=1200
WHITE=(255,255,255)
RED= (255,0,0)
BLUE =(0,0,204)


screen=pygame.display.set_mode((width,height)) # makes a screen
pygame.display.set_caption("falling stuff") 

clock= pygame.time.Clock() #games run on frames

FPS= 60 # game updates 60 times every second
running=True

# step 2. make user character object
# a object is a construct that holds both functions and data that 
#represent speific thing

class Player:# class 
    def __init__(self):
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
        pygame.draw.rect(screen, BLUE,(self.x, self.y,self.PlayerWidth ,self.playerHight))

class FallingObject:
    def __init__(self):
        self.x= random.randint(0,width-50)
        self.y=-50
        self.width=50
        self.height= 50
        self.speed= random.randint(5,200)
    
    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y > height

player=Player()
falling_object =[]
score = 0
lives =3
running = True


while running: 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    clock.tick(FPS)
    screen.fill(WHITE)
    
    keys=pygame.key.get_pressed()
    player.move(keys)
    player.draw()


    if random.randint(1, 3) ==1:# Lower the numbeer increase diff
        falling_object.append(FallingObject())
        
    #update falling objects
    for obj in falling_object[:]:
            obj.move()
            obj.draw()

      # Check for collision
            if (obj.x < player.x + player.PlayerWidth and
                obj.x + obj.width > player.x and
                obj.y < player.y + player.playerHight and
                obj.y + obj.height > player.y):
                lives -= 1
                falling_object.remove(obj)  # Remove object on collision

        # Remove objects off screen
            elif obj.off_screen():
                falling_object.remove(obj)
                score += 1  # Increase score for avoiding

    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    # Check game over
    if lives <= 0:
            game_over_text = font.render("Game Over!", True, (0, 0, 0))
            screen.blit(game_over_text, (width // 2 - 50, height // 2))
            pygame.display.update()
            pygame.time.delay(2000)  # Pause before quitting
            running = False



     #makes the game run like really thats this
    pygame.display.update()

pygame.quit()

