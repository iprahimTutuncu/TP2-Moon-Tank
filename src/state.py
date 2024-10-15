import pygame
from src.player import Player
from src.tilemap import TileMap
from src.ammunition import Ammunition
from src.goal import Goal

class State:
    def update(self):
        raise NotImplementedError("You must implement the update method.")

    def draw(self, surface):
        raise NotImplementedError("You must implement the draw method.")

    def input(self):
        raise NotImplementedError("You must implement the input method.")

class GameState:
    def __init__(self):
        self.BG_COLOR = (153, 178, 178)

        pygame.mixer.music.stop()
        pygame.mixer.music.load("./assets/rachmaninoff.mp3")
        pygame.mixer.music.play(-1)

        # Create entities
        self.player = Player()
        self.ammo_list = []
        # 0 = empty, 
        # 1 = wall,
        # 2 = green,
        # 3 = blue,
        # 4 = red,
        # 5 = floor

        map_data = [
            [1, 1, 1, 1, 1, 1, 5],
            [1, 5, 5, 5, 5, 4, 5],
            [1, 1, 1, 3, 3, 1, 1],
            [1, 0, 1, 5, 5, 1, 5],
            [1, 5, 2, 0, 0, 4, 5],
            [1, 1, 1, 0, 0, 1, 1]
        ]

        # 1 = red ammo
        # 2 = green ammo
        # 3 = blue ammo
        # 4 = condition de victoire, la class goal

        item_data = [
            [0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        self.tile_size = 96  # Size of each tile
        self.tilemap = TileMap(self.tile_size, map_data)
        self.tilemap.set_offset(224-96, 0) # le 96 c'est pour le mur caché pour pas aller à gauche
        self.player.set_offset(224-96, 0)
        
        for row_index, row in enumerate(item_data):
            for col_index, tile in enumerate(row):
                if tile == 4:
                    self.goal = Goal(col_index * self.tile_size, row_index * self.tile_size)
                    self.goal.set_offset(224-96, 0)
                elif tile > 0:
                    ammo = Ammunition(
                        col_index * self.tile_size + self.tile_size/2,
                        row_index * self.tile_size + self.tile_size/2,
                        'red' if tile == 1 else 'green' if tile == 2 else 'blue' if tile == 3 else 'unknown'
                    )
                    ammo.set_offset(224-96, 0)
                    self.ammo_list.append(ammo)

        self.bullet_group = pygame.sprite.Group()

    def update(self):
        previous_x = self.player.rect.x
        previous_y = self.player.rect.y

        self.player.update()
        self.bullet_group.update()

        wall_collisions = [tile for tile in pygame.sprite.spritecollide(self.player, self.tilemap.tiles, False) if tile.type != 5]
        for wall_collision in wall_collisions:
            print("Collided with a wall")
            self.player.rect.x = previous_x 
            self.player.rect.y = previous_y 
            break

        walls_to_remove = []
        for bullet in self.bullet_group:
            wall_collisions = [tile for tile in pygame.sprite.spritecollide(bullet, self.tilemap.tiles, False) if tile.type != 5]
            for wall in wall_collisions:
                print("Checking wall type:", wall.type)
                if bullet.bullet_type == 'red' and wall.type == 4:
                    print("Red bullet destroyed a wall")
                    walls_to_remove.append(wall)
                    bullet.kill()
                elif bullet.bullet_type == 'green' and wall.type == 2:
                    print("Green bullet destroyed a wall")
                    walls_to_remove.append(wall)
                    bullet.kill()
                elif bullet.bullet_type == 'blue' and wall.type == 3:
                    print("Blue bullet destroyed a wall")
                    walls_to_remove.append(wall)
                    bullet.kill()

        for wall in walls_to_remove:
            self.tilemap.tiles.remove(wall)

        ammo_to_remove = []

        for ammo in self.ammo_list:
            if ammo.rect.colliderect(self.player.rect):
                print(f"Collected {ammo.type} ammo")
                self.player.bullet_inventory[ammo.type] += 1
                ammo_to_remove.append(ammo)

        for ammo in ammo_to_remove:
            ammo.kill()
            self.ammo_list.remove(ammo)



    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.bullet_group)
                if event.key == pygame.K_z:
                    self.player.switch_bullet('red')
                elif event.key == pygame.K_x:
                    self.player.switch_bullet('blue')
                elif event.key == pygame.K_c:
                    self.player.switch_bullet('green')
                elif event.key == pygame.K_r:
                    return 'game'


        if self.goal.rect.colliderect(self.player.rect):
            return 'main_menu'

    def draw(self, screen):
        screen.fill(self.BG_COLOR)

        font = pygame.font.Font(None, 36)


        self.tilemap.draw(screen)
        for bullet in self.bullet_group:
            screen.blit(bullet.image, (bullet.rect.x + self.player.offset_x, bullet.rect.y + self.player.offset_y))
        self.player.draw(screen)
        for ammo in self.ammo_list:
            ammo.draw(screen)

        self.goal.draw(screen)

        rectangle_width = 224
        rectangle_height = screen.get_height()
        rectangle_color = (255, 255, 255)
        rectangle_position = (0, 0)

        pygame.draw.rect(screen, rectangle_color, (rectangle_position[0], rectangle_position[1], rectangle_width, rectangle_height))

        ammo_lines = []
        for color, count in self.player.bullet_inventory.items():
            if color == self.player.current_bullet:
                highlighted_text = f"{count} {color[0].upper()}" 
                ammo_lines.append((highlighted_text, (255, 215, 0)))
            else:
                if color == 'red':
                    text_color = (255, 0, 0)
                elif color == 'green':
                    text_color = (0, 255, 0)
                elif color == 'blue':
                    text_color = (0, 0, 255)
                else:
                    text_color = (0, 0, 0)

                ammo_lines.append((f"{count} {color[0].upper()}", text_color))

        for index, (line, color) in enumerate(ammo_lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(topleft=(10, 10 + index * 40))
            screen.blit(text_surface, text_rect)


        # Le "Press R to restart"
        restart_text = "Press R to restart"
        restart_text_surface = font.render(restart_text, True, (0, 0, 0))
        restart_text_rect = restart_text_surface.get_rect(center=(rectangle_width // 2, screen.get_height() - 30))
        screen.blit(restart_text_surface, restart_text_rect)

class MainMenuState(State):
    def __init__(self):
        self.options = ["Start Game", "Quit"]
        self.selected_index = 0  # curr selected option

    def update(self):
        pass

    def draw(self, surface):
        surface.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        
        for index, option in enumerate(self.options):
            color = (255, 215, 0) if index == self.selected_index else (0, 0, 0)  # Gold pour selected
            text = font.render(option, True, color)
            surface.blit(text, (100, 100 + index * 40))

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % len(self.options)  #down

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_index = (self.selected_index - 1) % len(self.options)  #up

                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 0:  # Start Game
                        return 'game'
                    elif self.selected_index == 1:  # Quit
                        return 'quit'

