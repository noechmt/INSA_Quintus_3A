import pygame

from GUI.title_screen import title_screen
from game_screen.game_screen import game_screen

if __name__ == "__main__":
    title_screen()
    game_screen()
    pygame.quit()
