from select import select
import pygame
from math import sqrt
import numpy as np
from Class.Cell import *
from Class.Button import Button
from Class.Map import *
from Class.Panel import Panel

# draw a rectangle with an opacity option

import sys

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
    width_wo_panel = WIDTH_SCREEN - (WIDTH_SCREEN/7)

    #taskbar
    color_brown = (70,46,1)
    bar = pygame.image.load("game_screen/game_screen_sprites/taskbar_background.png")
    SCREEN.blit(pygame.transform.scale(bar, (WIDTH_SCREEN, HEIGH_SCREEN/32)), (0, 0))
    taskbarfont = pygame.font.SysFont('courriernew',25) #police, size
    file_text = taskbarfont.render('File', False, color_brown)
    options_text = taskbarfont.render('Options', False, color_brown)
    help_text = taskbarfont.render('Help', False, color_brown)
    advisors_text = taskbarfont.render('Advisors', False, color_brown)
    SCREEN.blit(file_text, (WIDTH_SCREEN/60,HEIGH_SCREEN/256))
    SCREEN.blit(options_text, (WIDTH_SCREEN/16,HEIGH_SCREEN/256))
    SCREEN.blit(help_text, (WIDTH_SCREEN/7.5, HEIGH_SCREEN/256))
    SCREEN.blit(advisors_text, (WIDTH_SCREEN/5.5, HEIGH_SCREEN/256))

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    run = True
    clock = pygame.time.Clock()

    selection = {"is_active": False, "start": tuple, "cells": set()}
    hovered_cell = None
    zoom = 1
    move = 1

    walker_update_count = 0
    fire_upadte_count = 0



    ##############################
    while run:
        pos = pygame.mouse.get_pos()
        if pos[1] <= 60:
            map.offset_top += 10*(3 - pos[1] / 20)
            map.handle_move("up", 3 - pos[1] / 20)
            panel.display()
        if pos[1] >= HEIGH_SCREEN - 60:
            map.offset_top -= 10*(3 - (HEIGH_SCREEN - pos[1]) / 20)
            map.handle_move("down", 3 - (HEIGH_SCREEN - pos[1]) / 20)
            panel.display()
        if pos[0] <= 60:
            map.offset_left -= 10*(3 - pos[0] / 20)
            map.handle_move("left", 3 - pos[0] / 20)
            panel.display()
        if pos[0] >= WIDTH_SCREEN - 60:
            if not panel.get_road_button().is_hovered(pos) and not panel.get_well_button().is_hovered(pos):
                map.offset_left += 10*(3 - (WIDTH_SCREEN - pos[0]) / 20)
                map.handle_move("right", 3 - (WIDTH_SCREEN - pos[0]) / 20)
                panel.display()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            # Set and print logical coordinates
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 200, 100))
            x = round(((pos[1]-map.offset_top-HEIGH_SCREEN/6)/map.height_land - (
                WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0]-map.offset_left)/map.width_land))-1
            y = round(((WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0]-map.offset_left)/map.width_land + (
                pos[1]-map.offset_top-HEIGH_SCREEN/6)/map.height_land))
            text_click = fps_font.render(f"{x} {y}", 1, (255, 255, 255))
            SCREEN.blit(text_click, (0, 20))
            text_wallet = fps_font.render(f"{map.wallet}", 1, (255, 255, 255))
            SCREEN.blit(text_wallet, (0, 40))
            if event.type == pygame.QUIT:
                run = False
            # Move up
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if map.inMap(x, y) and not selection["is_active"]:
                        selection["start"] = (x, y)
                        selection["cells"].add((x, y))
                        selection["is_active"] = True

                # spawn the grid if is clicked
                    if (panel.get_grid_button().is_hovered(pos)):
                        map.grid_map()
                        panel.display()
                    if (panel.house_button.is_hovered(pos)):
                        panel.set_window("house")
                        map.handle_house_button()
                        map.display_map()
                    if (panel.shovel_button.is_hovered(pos)):
                        panel.set_window("shovel")
                        map.handle_shovel_button()
                        map.display_map()
                    if (panel.get_road_button().is_hovered(pos)):
                        panel.set_window("road")
                        map.handle_road_button()
                        map.display_map()
                    if (panel.prefecture_button.is_hovered(pos)):
                        panel.set_window("prefecture")
                        map.handle_prefecture_button()
                        map.display_map()
                    if (panel.engineerpost_button.is_hovered(pos)):
                        panel.set_window("engineer post")
                        map.handle_engineerpost_button()
                        map.display_map()
                    if (panel.well_button.is_hovered(pos)):
                        panel.set_window("well")
                        map.handle_well_button()
                        map.display_map()
                    # if pos[0] <= width_wo_panel:
                    #     map.handle_click_cells(pos)
                    #     panel.display()
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

            if event.type == pygame.MOUSEBUTTONUP:
                if selection["is_active"]:
                    for i in selection["cells"]:
                        selected_cell = map.get_cell(i[0], i[1])
                        if map.get_shoveled():
                            selected_cell.clear()
                        elif map.get_housed() and selected_cell.isBuildable():
                            selected_cell.build("house")
                        elif map.get_road_button_activated() and selected_cell.isBuildable():
                            selected_cell.build("path")
                        elif map.get_prefectured() and selected_cell.isBuildable():
                            selected_cell.build("prefecture")
                        elif map.get_engineered() and selected_cell.isBuildable():
                            selected_cell.build("engineer post")
                        elif map.get_welled() and selected_cell.isBuildable():
                            selected_cell.build("well")
                            for k in range(-2, 3):
                                for j in range(-2, 3):
                                    if (39>=x+k>=0 and 39>=y+j>=0):
                                        map.get_cell(i[0]+k, i[1]+j).display()
                        else:
                            selected_cell.display()
                    selection["cells"].clear()
                    selection["is_active"] = False

            if event.type == pygame.MOUSEMOTION:
                # Display previous cell without hover
                if hovered_cell:
                    hovered_cell = map.get_cell(hovered_coordinates[0], hovered_coordinates[1])
                    hovered_cell.display()
                    hovered_cell.display_around()
                if map.inMap(x, y) and pos[0] <= width_wo_panel and not selection["is_active"]:
                    hovered_coordinates = (x, y)
                    hovered_cell = map.get_cell(hovered_coordinates[0], hovered_coordinates[1])
                    hovered_cell.handle_hover_button()
                    hovered_cell.display_around()

                # Selection : fill the set with hovered cell
                if map.inMap(x, y) and selection["is_active"]:
                    for i in selection["cells"]:
                        map.get_cell(i[0], i[1]).display()
                    selection["cells"].clear()
                    range_x = range(
                        selection["start"][0], x+1, 1) if selection["start"][0] <= x else range(selection["start"][0], x-1, -1)
                    range_y = range(
                        selection["start"][1], y+1, 1) if selection["start"][1] <= y else range(selection["start"][1], y-1, -1)
                    for i in range_x:
                        for j in range_y:
                            selection["cells"].add((i, j))
                            map.get_cell(i, j).handle_hover_button()

                panel.get_grid_button().handle_hover_button(pos, SCREEN)
                panel.get_home_button().handle_hover_button(pos, SCREEN)
                panel.get_shovel_button().handle_hover_button(pos, SCREEN)
                panel.get_road_button().handle_hover_button(pos, SCREEN)
                panel.get_prefecture_button().handle_hover_button(pos, SCREEN)
                panel.get_engineerpost_button().handle_hover_button(pos, SCREEN)
                panel.get_well_button().handle_hover_button(pos, SCREEN)

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    panel.set_window("none")
                    map.handle_esc()

                # grid_button.handle_hover_button(pos, SCREEN)
                # home_button.handle_hover_button(pos, SCREEN)
                # shovel_button.handle_hover_button(pos, SCREEN)
                # road_button.handle_hover_button(pos, SCREEN)

        walker_update_count += 1
        # print(walker_update_count)
        if walker_update_count == 5:
            map.update_walkers()
            # print("break")
            walker_update_count = 0

        fire_upadte_count += 1
        if fire_upadte_count == 5 :
            map.update_fire()
            map.update_collapse()
            fire_upadte_count = 0
        
        # if tmpbool :
        #     map.array[13][29] = Prefecture(13, 29, map.height_land, map.width_land,map.screen, map)
        #     SCREEN.blit(pygame.transform.scale(pygame.image.load("walker_sprites/test/Housng1a_00019.png"), (map.array[13][29].width, map.array[13][29].height)), (map.array[13][29].left, map.array[13][29].top))
        #     map.array[31][19] = EngineerPost(31, 19, map.height_land, map.width_land, map.screen, map)
        #     SCREEN.blit(pygame.transform.scale(pygame.image.load("walker_sprites/test/Housng1a_00019.png"), (map.array[31][19].width, map.array[31][19].height)), (map.array[31][19].left, map.array[31][19].top))
        #     tmpbool = False
        clock.tick(60)
        fps = (int)(clock.get_fps())
        text_fps = fps_font.render(str(fps), 1, (255, 255, 255))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(
            0, HEIGH_SCREEN - text_fps.get_size()[1], 60, 40))
        SCREEN.blit(text_fps, (0, HEIGH_SCREEN - text_fps.get_size()[1]))
        pygame.display.flip()
