import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((96, 96))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.image.fill((255, 200, 200))
        
        self.render_text("SORTIE")

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def render_text(self, text):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 0, 0)) 
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)

        self.image.blit(text_surface, text_rect)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))
