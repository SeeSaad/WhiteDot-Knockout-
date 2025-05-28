import pygame

WHITE = (255, 255, 255)

# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y, radius=15, speed=200):
#         super().__init__()
#         self.radius = radius
#         self.speed = speed

#         self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
#         pygame.draw.circle(self.image, WHITE, (radius, radius), radius)

#         # Define the rect for positioning and collision
#         self.rect = self.image.get_rect(center=(x, y))

#     def handle_keys(self, keys, dt):
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= self.speed * dt
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += self.speed * dt
#         if keys[pygame.K_UP]:
#             self.rect.y -= self.speed * dt
#         if keys[pygame.K_DOWN]:
#             self.rect.y += self.speed * dt
#         print(self.rect.x, self.rect.y)

#     def update(self):
#         # Placeholder if you want to use sprite groups with `group.update()`
#         pass

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=15, max_speed=200, accel=600, damping=0.95):
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