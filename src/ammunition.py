import pygame
import math

class Ammunition(pygame.sprite.Sprite):
    def __init__(self, x, y, ammo_type):
        super().__init__()
        self.x = x
        self.y = y
        self.offset_x = 0
        self.offset_y = 0
        self.type = ammo_type
        
        # Set the size of the ammunition representation
        self.size = 20  # Size of the pentagon
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Draw the pentagon on the image surface
        self.render()

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def render(self):
        colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255)
        }

        color = colors.get(self.type, (255, 255, 255))

        self.image.fill((0, 0, 0, 0))

        points = []
        for i in range(5):
            angle = math.radians(i * 72) 
            x_offset = self.size * math.cos(angle) + self.size
            y_offset = self.size * math.sin(angle) + self.size
            points.append((x_offset, y_offset))

        pygame.draw.polygon(self.image, color, points)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))