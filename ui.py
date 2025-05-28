import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_menu(screen, width, best_time):
    font = pygame.font.SysFont(None, 48)

    screen.fill((0, 0, 0))
    
    title_text = font.render("Knockball Challenge!", True, (255, 255, 255))
    start_text = font.render("Press [SPACE] to Start", True, (255, 255, 255))
    quit_text = font.render("Press [ESC] to Quit", True, (255, 255, 255))

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 150))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, 250))
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 300))

    if best_time is not None:
        best_text = font.render(f"Best Time: {best_time:.2f}s", True, (255, 255, 255))
        screen.blit(best_text, (width // 2 - best_text.get_width() // 2, 400))

    pygame.display.flip()

def draw_pause_overlay(screen):
    font = pygame.font.SysFont(None, 60)
    pause_text = font.render("PAUSED", True, (255, 255, 255))
    sub_font = pygame.font.SysFont(None, 30)
    sub_text = sub_font.render("Press [Esc] to resume", True, (200, 200, 200))
    sub_text2 = sub_font.render("Press [R] to reset", True, (200, 200, 200))

    rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    sub_rect = sub_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
    sub_rect2 = sub_text2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 80))

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    screen.blit(pause_text, rect)
    screen.blit(sub_text, sub_rect)
    screen.blit(sub_text2, sub_rect2)

def show_result(screen, win: bool, elapsed_time, best_time):
    width = screen.get_width()
    height = screen.get_height()  # Fixed typo

    font = pygame.font.SysFont(None, 60)
    sub_font = pygame.font.SysFont(None, 30)

    text_main = "You Win!" if win else "that's all you got?"
    text_elapsed = f"Elapsed Time: {elapsed_time:.2f}s"
    text_best = f"Best Time: {best_time:.2f}s"

    color = (0, 255, 0) if win else (255, 0, 0)

    screen.fill(BLACK)

    # Render and blit main result
    main_surf = font.render(text_main, True, color)
    main_rect = main_surf.get_rect(center=(width // 2, height // 2 - 40))
    screen.blit(main_surf, main_rect)

    # Render and blit elapsed time
    elapsed_surf = sub_font.render(text_elapsed, True, WHITE)
    elapsed_rect = elapsed_surf.get_rect(center=(width // 2, height // 2 + 10))
    screen.blit(elapsed_surf, elapsed_rect)

    # Render and blit best time (even if user loses)
    best_surf = sub_font.render(text_best, True, WHITE)
    best_rect = best_surf.get_rect(center=(width // 2, height // 2 + 40))
    screen.blit(best_surf, best_rect)

    pygame.display.flip()
