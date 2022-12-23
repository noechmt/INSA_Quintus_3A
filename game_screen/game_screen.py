import pygame
from math import sqrt
import numpy as np
from Class.Cell import *
from Class.Button import Button
from Class.Map import *
from Class.Panel import Panel

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

    panel = Panel(SCREEN)

    # Dims without left panel
    height_wo_panel = HEIGH_SCREEN
    width_wo_panel = WIDTH_SCREEN - WIDTH_SCREEN / 7.5

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    run = True
    clock = pygame.time.Clock()
    zoom = 1
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # spawn the grid if is clicked
                    if (panel.get_grid_button().is_hovered(pos)):
                        map.grid_map()
                    if (panel.get_road_button().is_hovered(pos)):
                        panel.set_window("road")
                        map.handle_road_button()
                    if pos[0] <= width_wo_panel:
                        map.handle_click_cells(pos)
                # Zoom in
                if event.button == 4:
                    if zoom <= 1.25:
                        zoom += 0.01
                        SCREEN.fill((0, 0, 0))
                        for x in range(40):
                            for y in range(40):
                                map.get_cell(x, y).handle_zoom(1)
                        panel.display()
                if event.button == 5:
                    if zoom >= 0.95:
                        zoom -= 0.01
                        SCREEN.fill((0, 0, 0))
                        for x in range(40):
                            for y in range(40):
                                map.get_cell(x, y).handle_zoom(0)
                        panel.display()

            if event.type == pygame.MOUSEMOTION:
                if pos[0] <= width_wo_panel:
                    map.handle_hovered_cell(pos)
                panel.get_grid_button().handle_hover_button(pos, SCREEN)
                panel.get_home_button().handle_hover_button(pos, SCREEN)
                panel.get_shovel_button().handle_hover_button(pos, SCREEN)
                panel.get_road_button().handle_hover_button(pos, SCREEN)
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    panel.set_window("home")
                    map.handle_esc()

        clock.tick(60)
        fps = (int)(clock.get_fps())
        text_fps = fps_font.render(str(fps), 1, (255, 255, 255))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(
            0, HEIGH_SCREEN - text_fps.get_size()[1], 60, 40))
        SCREEN.blit(text_fps, (0, HEIGH_SCREEN - text_fps.get_size()[1]))
        pygame.display.flip()
