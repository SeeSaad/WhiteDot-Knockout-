import pygame
import sys
import random
import os

from player import Player
from enemies import Grey
from ui import draw_menu, draw_pause_overlay, show_result

WIDTH, HEIGHT = 800, 600
PLAYER_RADIUS = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen : pygame.Surface = None
game_state : str = "menu"

def load_best_time():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "best_time.txt")

    try:
        with open(file_path, "r") as f:
            best_time = float(f.read())
        return best_time
    except:
        return 999

def save_best_time(time):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "best_time.txt")
    with open(file_path, "w") as f:
        f.write(str(time))

def all_enemies_off_screen(enemies):
    for enemy in enemies:
        if -15 <= enemy.rect.centerx <= WIDTH +15 and -15 <= enemy.rect.centery <= HEIGHT + 15:
            return False
    return True

def menu():
    global game_state

    best_time = load_best_time()
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

        draw_menu(screen, WIDTH, best_time)

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

    paused = False
    win = False
    best_time = load_best_time()

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

    start_time = pygame.time.get_ticks()
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused

        if paused:
            screen.fill(BLACK)
            all_sprites.draw(screen)
            draw_pause_overlay(screen)
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        
        # if keys[pygame.K_r]:
        #     running = False

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
        
        if all_enemies_off_screen(enemies):
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed_time < best_time:
                save_best_time(elapsed_time)
                win = True
            show_result(screen, win, elapsed_time, best_time)
            pygame.time.wait(1500)
            running = False
            break

        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 36)
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_surface = font.render(f"Time: {elapsed_time:.2f}", True, (255, 255, 255))
        screen.blit(time_surface, (10, 10))
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
