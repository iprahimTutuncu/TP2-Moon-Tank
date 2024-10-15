import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, lifespan, bullet_type):
        super().__init__()
        self.radius = 5
        self.color = (255, 0, 0)
        self.bullet_type = bullet_type

        # Set bullet color based on type
        if bullet_type == 'red':
            self.color = (255, 0, 0)
        elif bullet_type == 'blue':
            self.color = (0, 0, 255)
        elif bullet_type == 'green':
            self.color = (0, 255, 0)

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect(center=(x, y))

        self.direction = direction
        self.speed = speed

        self.lifespan = lifespan
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if pygame.time.get_ticks() - self.start_time > self.lifespan:
            self.kill()
