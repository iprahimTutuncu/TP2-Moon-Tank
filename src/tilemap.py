import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, tile_type, image):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(x, y, width, height) 
        self.type = tile_type

class TileMap:
    def __init__(self, tile_size, map_data):
        self.tile_size = tile_size
        self.map_data = map_data
        self.tiles = pygame.sprite.Group()
        self.offset_x = 0
        self.offset_y = 0

        self.tile_images = {
            0: None,
            1: pygame.image.load('assets/wall.png'), 
            2: pygame.image.load('assets/green.png'),
            3: pygame.image.load('assets/blue.png'),
            4: pygame.image.load('assets/red.png'),
            5: pygame.image.load('assets/floor.png')
        }
        
        self.load_map()

    def load_map(self):
        self.tiles.empty()  # Clear existing tiles
        for row_index, row in enumerate(self.map_data):
            for col_index, tile in enumerate(row):
                if tile in self.tile_images:  # Check if tile type exists
                    tile_image = self.tile_images[tile]
                    if tile_image:
                        new_tile = Tile(
                            col_index * self.tile_size, 
                            row_index * self.tile_size, 
                            self.tile_size, 
                            self.tile_size, 
                            tile, 
                            tile_image
                        )
                        self.tiles.add(new_tile)

    def draw(self, surface):
        for tile in self.tiles:
            surface.blit(tile.image, (tile.rect.x + self.offset_x, tile.rect.y + self.offset_y))

    def update(self):
        self.tiles.update()

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y
