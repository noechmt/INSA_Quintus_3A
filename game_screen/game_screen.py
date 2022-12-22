import pygame
from math import sqrt
import numpy as np
from Class.Cell import *
from Class.Button import Button
from Class.Map import *

# draw a rectangle with an opacity option


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def game_screen():

    pygame.init()

    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    FPS = 60

    # Re-initialize the window
    SCREEN.fill((0, 0, 0))

    pygame.display.set_caption("Quintus III")
    WIDTH_SCREEN, HEIGH_SCREEN = SCREEN.get_size()
    height_land = HEIGH_SCREEN/60
    width_land = WIDTH_SCREEN*sqrt(2)/80
    SIZE = 40

    map = Map(SIZE, height_land, width_land, SCREEN)
    # background panel initialisation
    panel_background = pygame.image.load(
        "game_screen/game_screen_sprites/panel_background.png")
    for i in range(2):
        for j in range(9):
            SCREEN.blit(pygame.transform.scale(panel_background, (WIDTH_SCREEN/24,
                        HEIGH_SCREEN/10)), ((((i+22)/24)*WIDTH_SCREEN), (j/10)*HEIGH_SCREEN))
    draw_rect_alpha(SCREEN, (50, 50, 50, 60), (WIDTH_SCREEN *
                    (11/12), 0, WIDTH_SCREEN/12, HEIGH_SCREEN*9/10))

    # panel overlays initialisation (on the top of the panel)
    panel_overlays = pygame.image.load(
        "game_screen/game_screen_sprites/paneling_overlays.png")
    SCREEN.blit(pygame.transform.scale(panel_overlays, (WIDTH_SCREEN/18,
                HEIGH_SCREEN/36)), (11*WIDTH_SCREEN/12+5, HEIGH_SCREEN/32+2))

    # white rectangle under the button on the panel
    draw_rect_alpha(SCREEN, (255, 255, 255, 127), (177*WIDTH_SCREEN/192-2,
                    0.25*HEIGH_SCREEN-2, (WIDTH_SCREEN)/48+4, (HEIGH_SCREEN)/40+4))
    draw_rect_alpha(SCREEN, (255, 255, 255, 127), (182*WIDTH_SCREEN/192-2,
                    0.25*HEIGH_SCREEN-2, (WIDTH_SCREEN)/48+4, (HEIGH_SCREEN)/40+4))
    draw_rect_alpha(SCREEN, (255, 255, 255, 127), (187*WIDTH_SCREEN/192-2,
                    0.25*HEIGH_SCREEN-2, (WIDTH_SCREEN)/48+4, (HEIGH_SCREEN)/40+4))

    # window upside button initialisation
    panel_window_home = pygame.image.load(
        "game_screen/game_screen_sprites/panel_window_home.png")
    SCREEN.blit(pygame.transform.scale(panel_window_home, (WIDTH_SCREEN /
                12-10, HEIGH_SCREEN/17)), (11*WIDTH_SCREEN/12+5, 0.18*HEIGH_SCREEN))

    # panel grid button initialisation
    panel_grid_button = pygame.image.load(
        "game_screen/game_screen_sprites/paneling_grid_button.png")
    grid_button = Button(177*WIDTH_SCREEN/192, 0.125*HEIGH_SCREEN,
                         WIDTH_SCREEN/48, HEIGH_SCREEN/40, panel_grid_button)
    grid_button.draw(SCREEN)

    # panel home button initialisation
    panel_home_button = pygame.image.load(
        "game_screen/game_screen_sprites/paneling_home_button.png")
    home_button = Button(177*WIDTH_SCREEN/192, 0.25*HEIGH_SCREEN,
                         WIDTH_SCREEN/48, HEIGH_SCREEN/40, panel_home_button)
    home_button.draw(SCREEN)

    # panel shovel button initialisation
    panel_shovel_button = pygame.image.load(
        "game_screen/game_screen_sprites/paneling_shovel_button.png")
    shovel_button = Button(182*WIDTH_SCREEN/192, 0.25*HEIGH_SCREEN,
                           WIDTH_SCREEN/48, HEIGH_SCREEN/40, panel_shovel_button)
    shovel_button.draw(SCREEN)

    # panel road button initialisation
    panel_road_button = pygame.image.load(
        "game_screen/game_screen_sprites/paneling_road_button.png")
    road_button = Button(187*WIDTH_SCREEN/192, 0.25*HEIGH_SCREEN,
                         WIDTH_SCREEN/48, HEIGH_SCREEN/40, panel_road_button)
    road_button.draw(SCREEN)

    # panel information initialisation
    draw_rect_alpha(SCREEN, (25, 25, 25, 127), (WIDTH_SCREEN*(11/12)+2,
                    HEIGH_SCREEN*(8/17), WIDTH_SCREEN/12-4, 3*HEIGH_SCREEN/7-2))

    # bottom panel initialisation
    panel_bottom = pygame.image.load(
        "game_screen/game_screen_sprites/paneling_bot.png")
    SCREEN.blit(pygame.transform.scale(panel_bottom, (WIDTH_SCREEN/12,
                HEIGH_SCREEN/10)), (((11/12)*WIDTH_SCREEN), (0.9*HEIGH_SCREEN)))

    # Dims without left panel
    height_wo_panel = HEIGH_SCREEN
    width_wo_panel = WIDTH_SCREEN - (WIDTH_SCREEN/7)

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    run = True
    clock = pygame.time.Clock()
    while run:
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            x = round((pos[1]-HEIGH_SCREEN/6)/height_land - (WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0])/width_land)-1
            y = round((WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0])/width_land + (pos[1]-HEIGH_SCREEN/6)/height_land)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # spawn the grid if is clicked
                if (grid_button.is_hovered(pos)):
                    map.grid_map()
                if(home_button.is_hovered(pos)):
                    map.house_mod()
                if(map.array[x][y].is_hovered(pos) and map.get_housed()):
                    map.array[x][y].build("house")
            if event.type == pygame.MOUSEMOTION:
                map.handle_hovered_cell(pos)
                grid_button.handle_hover_button(pos, SCREEN)
                home_button.handle_hover_button(pos, SCREEN)
                shovel_button.handle_hover_button(pos, SCREEN)
                road_button.handle_hover_button(pos, SCREEN)
        clock.tick(60)
        fps = (int)(clock.get_fps())
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 60, 40))
        text_fps = fps_font.render(str(fps), 1, (255, 255, 255))
        SCREEN.blit(text_fps, (0, 0))
        pygame.display.flip()
