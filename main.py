import pygame
import sys

from src.state import State
from src.state import GameState
from src.state import MainMenuState

class StateManager:
    def __init__(self):
        self.states = []
        self.push(MainMenuState())

    def push(self, state):
        self.states.append(state)

    def pop(self):
        if self.states:
            self.states.pop()

    def current_state(self):
        return self.states[-1] if self.states else None

    def update(self):
        if self.states:
            state = self.current_state()
            action = state.input()
            if action == 'game':
                self.pop()
                self.push(GameState())
            elif action == 'main_menu':
                self.pop()
                self.push(MainMenuState())
            elif action == 'quit':
                pygame.quit()
                sys.exit()
            state.update()

    def draw(self, surface):
        if self.states:
            self.current_state().draw(surface)

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
