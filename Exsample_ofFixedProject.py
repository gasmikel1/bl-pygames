import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("cool name!")
game_over = False

WHITE = (255, 255, 255)
BLUE = (66, 135, 245)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

class Player:
    def __init__(self, x, y):
        self.health = 100 
        self.image = pygame.Surface((50, 50))
        self.attack_cooldown = 0
        self.attack_delay = 80
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel = [0, 0]
        self.speed = 7
        self.jump_power = -20
        self.gravity = 1
        self.on_ground = False
        self.attack = False

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
            self.attack = True
        else:
            self.attack = False

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
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"Player hit! Health: {self.health}")
        if self.health <= 0:
            print("Game Over")
            global game_over
            game_over = True

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, BLUE, (self.rect.x - scroll_x, self.rect.y, self.width, self.height))

    def attack_area(self):
        if self.vel[0] >= 0:
            return pygame.Rect(self.rect.right, self.rect.y + 10, 40, self.height - 20)
        else:
            return pygame.Rect(self.rect.left - 40, self.rect.y + 10, 40, self.height - 20)
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
#=============================
class Enemy:
    def __init__(self, x, y, width=40, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 2
        self.direction = 1
        self.movement_range = 200
        self.start_x = x
        self.patrol_speed = 2
        self.chase_speed = 4
        self.chase_range = 100
        self.attack_range = 10
        self.target = None
        self.attack_delay = 60
        self.attack_cooldown = 0
        self.damage = 10

        # Add gravity and vertical motion
        self.vel_y = 0
        self.gravity = 1
        self.on_ground = False


    def move(self, player, platforms):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.on_ground = False

    # Vertical collision
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0 and self.rect.bottom <= plat.top + self.vel_y:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

    # Check if player is within chase range and on same platform
        player_distance = abs(self.rect.centerx - player.rect.centerx)
        same_platform = abs(self.rect.bottom - player.rect.bottom) < 10

        if player_distance < self.chase_range and same_platform:
        # Chase player
            if player.rect.centerx < self.rect.centerx:
                self.direction = -2
        else:
            self.direction = 2
            move_speed = self.chase_speed
        
        # Patrol logic
            move_speed = self.patrol_speed
            if abs(self.rect.x - self.start_x) >= self.movement_range:
                self.direction *= -2

    # Edge detection before moving
            next_rect = self.rect.copy()
            next_rect.x += self.direction * move_speed
            ground_check_rect = next_rect.move(0, 1)
            ground_below = any(ground_check_rect.colliderect(plat) for plat in platforms)

            if ground_below:
                self.rect.x += self.direction * move_speed
            else:
                self.direction *= -10





       

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, RED, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))
    
    def check_for_player(self, player):
        if abs(self.rect.centerx - player.rect.centerx) <= self.chase_range:
            self.target = player
        else:
            self.target = None

    def update(self, player):
        if self.rect.colliderect(player.rect) and self.attack_cooldown == 0:
            player.take_damage(self.damage)
            self.attack_cooldown = self.attack_delay

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

#===============================================
def game_over_screen():
    font = pygame.font.SysFont("arial", 60)
    small_font = pygame.font.SysFont("arial", 40)

    try_again_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 20, 240, 60)
    quit_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 100, 240, 60)

    while True:
        screen.fill((30, 30, 30))
        title = font.render("Game Over", True, (255, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

        pygame.draw.rect(screen, (0, 200, 0), try_again_rect)
        pygame.draw.rect(screen, (200, 0, 0), quit_rect)

        try_again_text = small_font.render("Try Again", True, (255, 255, 255))
        quit_text = small_font.render("Quit", True, (255, 255, 255))

        screen.blit(try_again_text, (try_again_rect.centerx - try_again_text.get_width() // 2, try_again_rect.centery - try_again_text.get_height() // 2))
        screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_rect.collidepoint(event.pos):
                    return True  # Restart the game
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

platforms = [
    pygame.Rect(0, HEIGHT - 40, 2000, 40),
    pygame.Rect(300, HEIGHT - 150, 100, 20),
    pygame.Rect(500, HEIGHT - 250, 100, 20),
    pygame.Rect(750, HEIGHT - 180, 150, 20),
    pygame.Rect(1000, HEIGHT - 300, 100, 20),
    pygame.Rect(2000, HEIGHT - 5, 106, 200),
]

player = Player(100, HEIGHT - 150)
enemies = [Enemy(600, HEIGHT - 100), Enemy(1100, HEIGHT - 340)]

running = True
while running:
    # if game_over:
    #     print("Game Over")
    #     pygame.quit()
    #     sys.exit()

    if game_over:
        if game_over_screen():
            # Restart logic
            player = Player(100, HEIGHT - 150)
            enemies = [Enemy(600, HEIGHT - 100), Enemy(1100, HEIGHT - 340)]
            game_over = False
            continue

    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    attack_rect = player.attack_area() if player.attack else None

    player.apply_physics(platforms)

    for enemy in enemies[:]:
        enemy.check_for_player(player)
        enemy.update(player)
        if player.rect.colliderect(enemy.rect):
            if player.vel[1] > 0 and player.rect.bottom <= enemy.rect.top + player.vel[1]:
                enemies.remove(enemy)
                player.vel[1] = player.jump_power // 2
        
        if attack_rect and attack_rect.colliderect(enemy.rect):
            enemies.remove(enemy)

    scroll_x = player.rect.x - WIDTH // 2

    for enemy in enemies:
        enemy.move(player,platforms)
        enemy.draw(screen, scroll_x)

    for plat in platforms:
        pygame.draw.rect(screen, GREEN, (plat.x - scroll_x, plat.y, plat.width, plat.height))

    if attack_rect:
        pygame.draw.rect(screen, (0, 0, 0), (attack_rect.x - scroll_x, attack_rect.y, attack_rect.width, attack_rect.height), 2)

    player.draw(screen, scroll_x)
    player.update()
    pygame.display.flip()