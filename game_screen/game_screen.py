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
    width_panel = WIDTH_SCREEN / 7.5
    width_wo_panel = WIDTH_SCREEN - width_panel

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    run = True
    clock = pygame.time.Clock()
    zoom = 1
    move = 1
    while run:
        pos = pygame.mouse.get_pos()
        if move % 10 == 0:
            if pos[1] <= 60:
                map.handle_move("up", 3 - pos[1] / 20)
                panel.display()
            if pos[1] >= HEIGH_SCREEN - 60:
                map.handle_move("down", 3 - (HEIGH_SCREEN - pos[1]) / 20)
                panel.display()
            if pos[0] <= 60:
                map.handle_move("left", 3 - pos[0] / 20)
                panel.display()
            if pos[0] >= WIDTH_SCREEN - 60 and not panel.get_road_button().is_hovered(pos):
                map.handle_move("right", 3 - (WIDTH_SCREEN - pos[0]) / 20)
                panel.display()
            move = 0
        move += 1
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            x = round((pos[1]-HEIGH_SCREEN/6)/height_land -
                      (WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0])/width_land)-1
            y = round((WIDTH_SCREEN/2-WIDTH_SCREEN/12 -
                      pos[0])/width_land + (pos[1]-HEIGH_SCREEN/6)/height_land)
            if event.type == pygame.QUIT:
                run = False
            # Move up
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # spawn the grid if is clicked
                    if (panel.get_grid_button().is_hovered(pos)):
                        map.grid_map()
                        panel.display()
                    if (panel.get_road_button().is_hovered(pos)):
                        panel.set_window("road")
                        map.handle_road_button()
                    if (panel.home_button.is_hovered(pos)):
                        panel.set_window("house")
                        map.handle_house_button()
                    if pos[0] <= width_wo_panel:
                        map.handle_click_cells(pos)
                        panel.display()
                # Zoom in
                if event.button == 4:
                    if zoom <= 1.25:
                        zoom += 0.01
                        map.handle_zoom(1)
                        panel.display()
                if event.button == 5:
                    if zoom >= 0.95:
                        zoom -= 0.01
                        map.handle_zoom(0)
                        panel.display()
                if (map.array[x][y].is_hovered(pos) and map.get_housed()):
                    print(x, y)
                    map.array[x][y].build("house")
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
