import pygame
from src.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('./assets/tank.png')
        self.shoot_sound = pygame.mixer.Sound("assets/cannon_fire.ogg")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(150, 140))
        self.speed = 6
        self.offset_x = 0
        self.offset_y = 0
        self.direction = 'right'  # Default direction

        self.bullet_inventory = {
            'red': 2,
            'blue': 0,
            'green': 0
        }

        self.current_bullet = 'red'

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 'right'
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = 'up'
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = 'down'
        
        self.update_image()

    def update_image(self):
        if self.direction == 'left':
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == 'right':
            self.image = self.original_image
        elif self.direction == 'up':
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.original_image, 270)

        self.rect = self.image.get_rect(center=self.rect.center)

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))

    def shoot(self, bullet_group):
        if self.bullet_inventory[self.current_bullet] > 0:
            bullet_direction = (0, 0)
            if self.direction == 'left':
                bullet_direction = (-1, 0)
            elif self.direction == 'right':
                bullet_direction = (1, 0)
            elif self.direction == 'up':
                bullet_direction = (0, -1)
            elif self.direction == 'down':
                bullet_direction = (0, 1)

            bullet_speed = 15
            bullet_lifespan = 2000
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, bullet_direction, bullet_speed, bullet_lifespan, self.current_bullet)
            bullet_group.add(bullet)

            self.bullet_inventory[self.current_bullet] -= 1

            self.shoot_sound.play()

    def switch_bullet(self, bullet_type):
        if bullet_type in self.bullet_inventory:
            self.current_bullet = bullet_type