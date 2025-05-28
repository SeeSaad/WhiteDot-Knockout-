import pygame
import random

GREY = (160, 160, 160)

class Grey(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=15):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREY, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

        self.position = pygame.Vector2(x, y)
        # self.velocity = pygame.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))  # random motion
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
