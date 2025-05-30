import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("cool name!")

# ============================
# Step 2: Define Colors
# ============================
WHITE = (255, 255, 255)
BLUE = (66, 135, 245)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# ============================
# Step 3: Classes
# ============================

class Player:
    def __init__(self, x, y):
        self.image =pygame.Surface((50,50))
        self.attack_cooldown = 0
        self.attack_delay =80  # 500ms cooldown between attacks
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel = [0, 0]
        self.speed = 7
        self.jump_power = -20
        self.gravity = 1
        self.on_ground = False
        #self.attack=False

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.vel[0] = -self.speed
        elif keys[pygame.K_d]:
            self.vel[0] = self.speed
        else:
            self.vel[0] = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel[1] = self.jump_power
            self.on_ground = False
        elif keys[pygame.K_e] and self.attack_cooldown == 0:
            self.attack_cooldown = self.attack_delay
            self.attack=True
        else:
            self.attack=False

class SlashEffect:
    def __init__(self, x, y, facing_right):
        self.duration = 10  # frames the effect will last
        self.counter = 0
        self.rect = pygame.Rect(x, y, 40, 40)
        self.facing_right = facing_right

    def update(self):
        self.counter += 1

    def is_alive(self):
        return self.counter < self.duration

    def draw(self, surface, scroll_x):
        color = (0, 0, 0)
        if self.facing_right:
            pygame.draw.line(surface, color, (self.rect.x - scroll_x, self.rect.y),
                             (self.rect.x + self.rect.width - scroll_x, self.rect.y + self.rect.height), 3)
        else:
            pygame.draw.line(surface, color, (self.rect.x + self.rect.width - scroll_x, self.rect.y),
                             (self.rect.x - scroll_x, self.rect.y + self.rect.height), 3)




    def apply_physics(self, platforms):
        self.vel[1] += self.gravity
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel[1] > 0 and self.rect.bottom <= plat.top + self.vel[1]:
                    self.rect.bottom = plat.top
                    self.vel[1] = 0
                    self.on_ground = True

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, BLUE, (self.rect.x - scroll_x, self.rect.y, self.width, self.height))

    def attack_area(self):
        if self.vel[0] >= 0:
            attack_rect = pygame.Rect(self.rect.right, self.rect.y + 10, 40, self.height - 20)
        else: 
            attack_rect = pygame.Rect(self.rect.left - 40 , self.rect.y + 10, 40, self.height - 20)
        return attack_rect
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
#--------------------------
#Enemy ai
#--------------------------
class Enemy:
    def __init__(self, x, y, width=40, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 2
        self.direction = 1
        self.movement_range = 100
        self.start_x = x
        self.patrol_speed = 2  # Patrolling speed
        self.chase_speed = 4  # Chasing speed
        self.chase_range = 100  # Distance at which enemy starts chasing player
        self.attack_range = 50  # Distance to attack player
        self.target = None  # The target (player)
    
    def move(self, player):
        # Get the direction of movement based on patrolling or chasing
        if self.target:
            # Chase the player
            if self.rect.x < self.target.rect.x - self.attack_range:
                self.rect.x += self.chase_speed  # Move towards the player
            elif self.rect.x > self.target.rect.x + self.attack_range:
                self.rect.x -= self.chase_speed  # Move towards the player
        else:
            # Patrolling logic
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.start_x) >= self.movement_range:
                self.direction *= -1  # Change direction

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, RED, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))
    
    def check_for_player(self, player):
        # Check if the player is within the chase range
        if abs(self.rect.centerx - player.rect.centerx) <= self.chase_range:
            self.target = player  # Start chasing the player
        else:
            self.target = None  # Stop chasing, go back to patrolling
        
        # Change direction at the bounds
        
# ============================
# Step 4: Platforms
# ============================
platforms = [
    pygame.Rect(0, HEIGHT - 40, 2000, 40),
    pygame.Rect(300, HEIGHT - 150, 100, 20),
    pygame.Rect(500, HEIGHT - 250, 100, 20),
    pygame.Rect(750, HEIGHT - 180, 150, 20),
    pygame.Rect(1000, HEIGHT - 300, 100, 20),
    pygame.Rect(0,HEIGHT-50,100,2),
    ]

# ============================
# Step 5: Create Player and Enemies
# ============================
player = Player(100, HEIGHT - 150)
enemies = [Enemy(600, HEIGHT - 100), Enemy(1100, HEIGHT - 340)]

# ============================
# Step 6: Game Loop
# ============================
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # ============================
    # Step 7: Event Handling
    # ============================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ============================
    # Step 8: Input
    # ============================
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    #attack_rect = None
    #if player.attack:
    #    attack_rect = player.attack_area()
    attack_rect = None
    if player.attack:
        attack_rect = player.attack_area()
        slash_effects.append(SlashEffect(attack_rect.x, attack_rect.y, player.facing_right))



    # ============================
    # Step 9: Physics
    # ============================
    player.apply_physics(platforms)

    # ============================
    # Step 10: Enemy Collision
    # ============================
    for enemy in enemies[:]:
        enemy.check_for_player(player) 
        if player.rect.colliderect(enemy.rect):
            if player.vel[1] > 0 and player.rect.bottom <= enemy.rect.top + player.vel[1]:
                enemies.remove(enemy)
                player.vel[1] = player.jump_power // 2  # Bounce
       
        if attack_rect:
            for enemy in enemies[:]:
                if attack_rect.colliderect(enemy.rect):
                    enemies.remove(enemy)  

    # ============================
    # Step 11: Camera Scroll
    # ============================
    scroll_x = player.rect.x - WIDTH // 2

    # ============================
    # Step 12: Drawing
    # ============================
    
    for enemy in enemies:
        enemy.move(player)  # Pass player to move method to chase
        enemy.draw(screen, scroll_x)
    for plat in platforms:

        pygame.draw.rect(screen, GREEN, (plat.x - scroll_x, plat.y, plat.width, plat.height))

    slash_effects = []
    if attack_rect:
       pygame.draw.rect(screen, (0, 0, 0), (attack_rect.x - scroll_x, attack_rect.y, attack_rect.width, attack_rect.height), 2)
    
    for effect in slash_effects[:]:
        effect.update()
    if not effect.is_alive():
        slash_effects.remove(effect)
    else:
        effect.draw(screen, scroll_x)
    player.draw(screen, scroll_x)
    player.update()  # Reduce attack cooldown

    pygame.display.flip()
