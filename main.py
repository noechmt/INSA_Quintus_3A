from game_screen.game_screen import game_screen
from GUI.title_screen import title_screen
import pygame
import sys
import os

# Check of the version of python
assert sys.version[0:4] == "3.10", "Merci d'utiliser une version de python >= 3.10 !"

# Check if all the dependencies are installed
os.system(str(sys.executable) + " -m pip install -r requirements.txt")

if __name__ == "__main__":
    if (title_screen()):
        game_screen()
    pygame.quit()


# TODO
# risques avec l'overlay
# prefect -> éteindre le feu
# sauvegarde
# well + water overlay
