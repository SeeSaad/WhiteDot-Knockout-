import pygame

WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=15, max_speed=250, accel=600, damping=0.95):
        super().__init__()
        self.radius = radius
        self.max_speed = max_speed
        self.acceleration = accel
        self.damping = damping

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

    def handle_input(self, keys, dt):
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT]:
            direction.x += -1
        if keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_UP]:
            direction.y += -1
        if keys[pygame.K_DOWN]:
            direction.y += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.velocity += direction * self.acceleration * dt
        else:
            self.velocity *= self.damping

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
