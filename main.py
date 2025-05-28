import pygame
import sys
import random

from player import Player
from enemies import Grey
from ui import draw_menu

WIDTH, HEIGHT = 800, 600
PLAYER_RADIUS = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen : pygame.Surface = None
game_state : str = "menu"

def menu():
    global game_state

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "game"
            break

        elif keys[pygame.K_ESCAPE]:
            game_state = "quit"
            break

        draw_menu(screen, WIDTH)

def resolve_collision(a, b):
    """Elastic collision response between two circular sprites (a and b)."""
    pos_a = pygame.Vector2(a.position)
    pos_b = pygame.Vector2(b.position)
    delta = pos_b - pos_a
    distance = delta.length()

    if distance == 0:
        return  # Avoid divide-by-zero

    overlap = a.radius + b.radius - distance
    if overlap > 0:
        # Move them apart
        correction = delta.normalize() * (overlap / 2)
        a.position -= correction
        b.position += correction

        # Reflect velocities along the collision normal
        normal = delta.normalize()
        rel_vel = b.velocity - a.velocity
        sep_velocity = rel_vel.dot(normal)

        if sep_velocity < 0:
            impulse = normal * sep_velocity
            a.velocity += impulse
            b.velocity -= impulse


def game():
    global game_state

    NUM_ENEMIES = 10

    dt = 0
    
    player = Player(WIDTH // 2, HEIGHT // 2)

    enemies = pygame.sprite.Group()
    for _ in range(NUM_ENEMIES):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        enemies.add(Grey(x, y))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"
                running = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_r]:
            running = False

        player.handle_input(keys, dt)

        all_sprites.update(dt)

        handled_pairs = set()

        enemy_list = list(enemies)
        for i in range(len(enemy_list)):
            for j in range(i + 1, len(enemy_list)):
                a = enemy_list[i]
                b = enemy_list[j]
                if pygame.sprite.collide_circle(a, b):
                    pair = tuple(sorted((id(a), id(b))))
                    if pair not in handled_pairs:
                        resolve_collision(a, b)
                        handled_pairs.add(pair)
        
        for enemy in enemies:
            if pygame.sprite.collide_circle(player, enemy):
                pair = tuple(sorted((id(player), id(enemy))))
                if pair not in handled_pairs:
                    resolve_collision(player, enemy)
                    handled_pairs.add(pair)

        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

def main():
    global screen, game_state
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WhiteDot Knockout")

    game_state = "menu"
    
    while game_state != "quit":
        if game_state == "menu":
            menu()
        elif game_state == "game":
            game()
        else:
            print(game_state)
            break

    pygame.quit()
    sys.exit()

main()

# def main():
#     pygame.init()


#     WIDTH, HEIGHT = 800, 600
#     PLAYER_RADIUS = 15
#     PLAYER_SPEED = 5
#     BLACK = (0, 0, 0)
#     WHITE = (255, 255, 255)

#     NUM_ENEMIES = 10

#     dt = 0

#     handled_pairs = set()

#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("WhiteDot SURVIVE")

#     player = Player(WIDTH // 2, HEIGHT // 2)

#     enemies = pygame.sprite.Group()
#     for _ in range(NUM_ENEMIES):
#         x = random.randint(50, WIDTH - 50)
#         y = random.randint(50, HEIGHT - 50)
#         enemies.add(Grey(x, y))

#     all_sprites = pygame.sprite.Group()
#     all_sprites.add(player)
#     all_sprites.add(enemies)

#     clock = pygame.time.Clock()
#     running = True
#     while running:
#         dt = clock.tick(60) / 1000

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         keys = pygame.key.get_pressed()
#         player.handle_input(keys, dt)

#         all_sprites.update(dt)

#         if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle):
#             print("Player collided with an enemy!")

#         enemy_list = list(enemies)
#         for i in range(len(enemy_list)):
#             for j in range(i + 1, len(enemy_list)):
#                 if pygame.sprite.collide_circle(enemy_list[i], enemy_list[j]):
#                     print("Enemy-to-enemy collision!")

#         screen.fill(BLACK)
#         all_sprites.draw(screen)
#         pygame.display.flip()


#     pygame.quit()
#     sys.exit()

# main()