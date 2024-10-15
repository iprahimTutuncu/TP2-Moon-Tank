import pygame
import sys

from src.state_manager import StateManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.mixer.init()
    clock = pygame.time.Clock()
    state_manager = StateManager()

    while True:
        state_manager.update()
        state_manager.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
