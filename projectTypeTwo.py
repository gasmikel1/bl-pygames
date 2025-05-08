import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("cool name!")

WHITE = (255, 255, 255)
BLUE = (66, 135, 245)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Arial", 36)

def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont("Arial", size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)

class Slash:
    def __init__(self, x, y, direction):
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.arc(self.image, YELLOW, (0, 0, 40, 40), 0, 3.14, 4)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 10
        self.direction = direction

    def update(self):
        self.life -= 1

    def draw(self, surface, scroll_x):
        surface.blit(self.image, (self.rect.x - scroll_x, self.rect.y))

class Player:
    def __init__(self, x, y):
        self.health = 100
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel = [0, 0]
        self.speed = 7
        self.jump_power = -20
        self.gravity = 1
        self.on_ground = False
        self.attack = False
        self.attack_cooldown = 0
        self.attack_delay = 30
        self.attacked_this_frame = False
        self.slashes = []
        self.facing_right = True  # Track facing direction

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.vel[0] = -self.speed
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.vel[0] = self.speed
            self.facing_right = True
        else:
            self.vel[0] = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel[1] = self.jump_power
            self.on_ground = False
        elif keys[pygame.K_e] and self.attack_cooldown == 0:
            self.attack_cooldown = self.attack_delay
            self.attack = True
            self.attacked_this_frame = True
            self.spawn_slash()
        else:
            self.attack = False
            self.attacked_this_frame = False

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

    def take_damage(self, amount, knockback_dir=1):
        self.health -= amount
        print(f"Player hit! Health: {self.health}")
        self.rect.x += knockback_dir * 20
        self.vel[1] = -8
        self.attack = False
        if self.health <= 0:
            return True
        return False

    def attack_area(self):
        reach = 60
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.y + 10, reach, self.height - 20)
        else:
            return pygame.Rect(self.rect.left - reach, self.rect.y + 10, reach, self.height - 20)

    def spawn_slash(self):
        direction = 1 if self.facing_right else -1
        x = self.rect.right if direction == 1 else self.rect.left - 40
        y = self.rect.centery - 20
        self.slashes.append(Slash(x, y, direction))

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        for slash in self.slashes[:]:
            slash.update()
            if slash.life <= 0:
                self.slashes.remove(slash)

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, BLUE, (self.rect.x - scroll_x, self.rect.y, self.width, self.height))
        for slash in self.slashes:
            slash.draw(surface, scroll_x)

class Enemy:
    def __init__(self, x, y, width=40, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = 30
        self.speed = 2
        self.direction = 1
        self.movement_range = 200
        self.start_x = x
        self.patrol_speed = 1
        self.chase_speed = 4
        self.chase_range = 100
        self.attack_delay = 60
        self.attack_cooldown = 0
        self.damage = 15
        self.vel_y = 0
        self.gravity = 1
        self.on_ground = False
        self.stun_timer = 0

    def move(self, player, platforms):
        if self.stun_timer > 0:
            self.stun_timer -= 1
            return

        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0 and self.rect.bottom <= plat.top + self.vel_y:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

        player_distance = abs(self.rect.centerx - player.rect.centerx)
        same_platform = abs(self.rect.bottom - player.rect.bottom) < 10

        if player_distance < self.chase_range and same_platform:
            self.direction = -1 if player.rect.centerx < self.rect.centerx else 1
            move_speed = self.chase_speed
        else:
            move_speed = self.patrol_speed

        if abs(self.rect.x - self.start_x) >= self.movement_range:
            self.direction *= -1

        next_rect = self.rect.copy()
        next_rect.x += self.direction * move_speed
        ground_check_rect = next_rect.move(0, 1)
        ground_below = any(ground_check_rect.colliderect(plat) for plat in platforms)

        if ground_below:
            self.rect.x += self.direction * move_speed
        else:
            self.direction *= -1

    def take_damage(self, amount, knockback_dir=1):
        self.health -= amount
        self.rect.x += knockback_dir * 20
        self.vel_y = -5
        self.stun_timer = 30
        return self.health <= 0

    def update(self, player):
        if self.stun_timer <= 0 and self.rect.colliderect(player.rect) and self.attack_cooldown == 0:
            knockback_direction = 1 if self.rect.centerx < player.rect.centerx else -1
            if player.take_damage(self.damage, knockback_direction):
                return True
            self.attack_cooldown = self.attack_delay

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        return False

    def draw(self, surface, scroll_x):
        pygame.draw.rect(surface, RED, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))

def draw_health_bar(surface, x, y, health, max_health):
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    fill = (health / max_health) * BAR_WIDTH
    pygame.draw.rect(surface, RED, (x, y, BAR_WIDTH, BAR_HEIGHT), 2)
    pygame.draw.rect(surface, GREEN, (x, y, fill, BAR_HEIGHT))

def show_end_screen(message):
    while True:
        screen.fill(WHITE)
        draw_text(screen, message, 64, WIDTH // 2, HEIGHT // 3)
        draw_text(screen, "Press R to Restart or Q to Quit", 32, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return True
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def start_game():
    global player, enemies
    platforms = [
        pygame.Rect(0, HEIGHT - 40, 2000, 40),
        pygame.Rect(300, HEIGHT - 150, 100, 20),
        pygame.Rect(500, HEIGHT - 250, 100, 20),
        pygame.Rect(750, HEIGHT - 180, 150, 20),
        pygame.Rect(1000, HEIGHT - 300, 100, 20),
        pygame.Rect(2000, HEIGHT - 5, 106, 200),
    ]
    goal = pygame.Rect(1900, HEIGHT - 100, 50, 80)
    player = Player(100, HEIGHT - 150)
    enemies = [Enemy(600, HEIGHT - 100), Enemy(1100, HEIGHT - 340)]
    return platforms, goal

platforms, goal = start_game()

running = True
while running:
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
        if enemy.update(player):
            if show_end_screen("Game Over"):
                platforms, goal = start_game()
                continue

        if player.rect.colliderect(enemy.rect):
            if player.vel[1] > 0 and player.rect.bottom <= enemy.rect.top + player.vel[1]:
                enemies.remove(enemy)
                player.vel[1] = player.jump_power // 2
        if player.attacked_this_frame and attack_rect and attack_rect.colliderect(enemy.rect):
            knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
            if enemy.take_damage(15, knockback_direction):
                enemies.remove(enemy)

    if player.rect.y > HEIGHT + 200:
        if player.take_damage(player.health):
            if show_end_screen("Game Over"):
                platforms, goal = start_game()
                continue

    scroll_x = player.rect.x - WIDTH // 2
    pygame.draw.rect(screen, (255, 215, 0), (goal.x - scroll_x, goal.y, goal.width, goal.height))

    if player.rect.colliderect(goal):
        if show_end_screen("You Win!"):
            platforms, goal = start_game()
            continue

    for enemy in enemies:
        enemy.move(player, platforms)
        enemy.draw(screen, scroll_x)

    for plat in platforms:
        pygame.draw.rect(screen, GREEN, (plat.x - scroll_x, plat.y, plat.width, plat.height))

    player.draw(screen, scroll_x)
    player.update()
    draw_health_bar(screen, 20, 20, player.health, 100)
    pygame.display.flip()
