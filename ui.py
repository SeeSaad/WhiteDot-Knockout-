import pygame

def draw_menu(screen, width):
    font = pygame.font.SysFont(None, 48)
    best_time = 9999

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