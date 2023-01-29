from select import select
from tabnanny import check
import pygame
import pickle
from math import sqrt
import numpy as np
from Class.Button import Button
from Class.Map import *
from Class.Panel import Panel
import time
from datetime import datetime

# draw a rectangle with an opacity option


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def game_screen():

    pygame.init()

    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    set_SCREEN(SCREEN)
    FPS = 60

    # Re-initialize the window
    SCREEN.fill((0, 0, 0))

    pygame.mixer.init()
    pygame.mixer.music.load("audio/tunic_ost.wav")
    pygame.mixer.music.play(-1)
    # print(pygame.mixer.music.get_volume())
    pygame.mixer.music.set_volume(0.05)

    pygame.display.set_caption("Quintus III")
    WIDTH_SCREEN, HEIGH_SCREEN = SCREEN.get_size()
    height_land = HEIGH_SCREEN/60
    width_land = WIDTH_SCREEN*sqrt(2)/80
    SIZE = 40

    # Load new map or existing one with pickle
    file = open("Saves/.temp.txt", "r")
    name_path = file.read()
    if "Saves/" in name_path:
        with open(name_path, 'rb') as f1:
            map = pickle.load(f1)
        map.display_map()
    else:
        map = Map(SIZE, height_land, width_land)
        map.set_name_user(name_path)

    panel = Panel(SCREEN)

    # Dims without left panel
    height_wo_panel = HEIGH_SCREEN
    width_wo_panel = WIDTH_SCREEN - (WIDTH_SCREEN/7)

# taskbar
    """color_brown = (70, 46, 1)
    bar = pygame.image.load(
        "game_screen/game_screen_sprites/taskbar_background.png")
    SCREEN.blit(pygame.transform.scale(
        bar, (WIDTH_SCREEN, HEIGH_SCREEN/32)), (0, 0))
    taskbarfont = pygame.font.SysFont('courriernew', 25)  # police, size
    file_text = taskbarfont.render('File', 0, color_brown)
    options_text = taskbarfont.render('Options', 0, color_brown)
    help_text = taskbarfont.render('Help', 0, color_brown)
    advisors_text = taskbarfont.render('Advisors', 0, color_brown)
    SCREEN.blit(file_text, (WIDTH_SCREEN/60, HEIGH_SCREEN/256))
    SCREEN.blit(options_text, (WIDTH_SCREEN/16, HEIGH_SCREEN/256))
    SCREEN.blit(help_text, (WIDTH_SCREEN/7.5, HEIGH_SCREEN/256))
    SCREEN.blit(advisors_text, (WIDTH_SCREEN/5.5, HEIGH_SCREEN/256))"""

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    run = 1
    clock = pygame.time.Clock()

    speeds = [0.000000001, 0.4, 0.6, 0.8, 1, 1.25, 1.5, 2, 3, 5]
    speed_index = 4
    speed = speeds[speed_index]
    speed_left = 186.5*WIDTH_SCREEN/192
    speed_top = 0.25*HEIGH_SCREEN+12.5*HEIGH_SCREEN/80
    speed_counter_text = fps_font.render(
        f"{speed * 100:.0f}%", 1, (255, 255, 255))
    SCREEN.blit(speed_counter_text, (speed_left, speed_top))
    paused = 0

    selection = {"is_active": 0, "start": tuple, "cells": set()}
    hovered_cell = None
    zoom = 1
    move = 1
    zoom_update = 0

    walker_update_count = 0
    fire_upadte_count = 0
    current_time = ""
    ##############################
    while run:

        pos = pygame.mouse.get_pos()
        if pos[1] <= 60:
            map.offset_top += 5*(3 - pos[1] / 20)*zoom
            map.handle_move("up", (3 - pos[1] / 20)*zoom)
            panel.display()
            speed_counter_text = fps_font.render(
                f"{speed * 100:.0f}%", 1, (255, 255, 255))
            SCREEN.blit(speed_counter_text, (speed_left, speed_top))
        if pos[1] >= HEIGH_SCREEN - 60:
            map.offset_top -= 5*(3 - (HEIGH_SCREEN - pos[1]) / 20)*zoom
            map.handle_move("down", (3 - (HEIGH_SCREEN - pos[1]) / 20) * zoom)
            panel.display()
            speed_counter_text = fps_font.render(
                f"{speed * 100:.0f}%", 1, (255, 255, 255))
            SCREEN.blit(speed_counter_text, (speed_left, speed_top))
        if pos[0] <= 60:
            map.offset_left -= 5*(3 - pos[0] / 20)*zoom
            map.handle_move("left", (3 - pos[0] / 20)*zoom)
            panel.display()
            speed_counter_text = fps_font.render(
                f"{speed * 100:.0f}%", 1, (255, 255, 255))
            SCREEN.blit(speed_counter_text, (speed_left, speed_top))
        if pos[0] >= WIDTH_SCREEN - 60:
            if not panel.get_road_button().is_hovered(pos) and not panel.get_well_button().is_hovered(pos):
                map.offset_left += 5*(3 - (WIDTH_SCREEN - pos[0]) / 20)*zoom
                map.handle_move(
                    "right", (3 - (WIDTH_SCREEN - pos[0]) / 20) * zoom)
                panel.display()
                speed_counter_text = fps_font.render(
                    f"{speed * 100:.0f}%", 1, (255, 255, 255))
                SCREEN.blit(speed_counter_text, (speed_left, speed_top))
        zoom_update += 1
        for event in pygame.event.get():
            if map.get_overlay() in ("fire", "collapse"):
                map.display_overlay()
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
                """with open('not_empty_map', 'wb') as f1:
                    pickle.dump(map, f1)"""
                run = 0
            # Move up
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if map.inMap(x, y) and not selection["is_active"]:
                        selection["start"] = (x, y)
                        selection["cells"].add((x, y))
                        selection["is_active"] = 1

                # spawn the grid if is clicked
                    if (panel.get_grid_button().is_hovered(pos)):
                        map.set_overlay("grid")
                        panel.display()
                        speed_counter_text = fps_font.render(
                            f"{speed * 100:.0f}%", 1, (255, 255, 255))
                        SCREEN.blit(speed_counter_text,
                                    (speed_left, speed_top))
                    if (panel.house_button.is_hovered(pos)):
                        panel.set_window("house")
                        map.handle_button("house")
                        map.set_overlay("")
                    if (panel.shovel_button.is_hovered(pos)):
                        panel.set_window("shovel")
                        map.handle_button("shovel")
                        map.set_overlay("")
                        # map.display_map()
                    if (panel.get_road_button().is_hovered(pos)):
                        panel.set_window("road")
                        map.handle_button("road")
                        map.set_overlay("")
                        # map.display_map()
                    if (panel.prefecture_button.is_hovered(pos)):
                        panel.set_window("prefecture")
                        map.handle_button("prefecture")
                        map.set_overlay("")
                        # map.display_map()
                    if (panel.engineerpost_button.is_hovered(pos)):
                        panel.set_window("engineer post")
                        map.handle_button("engineerpost")
                        map.set_overlay("")
                        # map.display_map()
                    if (panel.well_button.is_hovered(pos)):
                        panel.set_window("well")
                        map.handle_button("well")
                        map.set_overlay("water")
                        # map.display_map()
                    if (panel.up_button.is_hovered(pos)):
                        if speed_index < 9:
                            speed_index += 1
                            speed = speeds[speed_index]
                            panel.set_played_button()
                            panel.display()
                            speed_counter_text = fps_font.render(
                                f"{speed * 100:.0f}%", 1, (255, 255, 255))
                            SCREEN.blit(speed_counter_text,
                                        (speed_left, speed_top))
                    if (panel.down_button.is_hovered(pos)):
                        if (speed_index > 1):
                            speed_index -= 1
                            speed = speeds[speed_index]
                            panel.set_played_button()
                            panel.display()
                            speed_counter_text = fps_font.render(
                                f"{speed * 100:.0f}%", 1, (255, 255, 255))
                            SCREEN.blit(speed_counter_text,
                                        (speed_left, speed_top))
                    if (panel.get_pause_button().is_hovered(pos)):
                        if paused == 0:
                            paused = 1
                            speed = speeds[0]
                            panel.set_paused_button()
                            panel.display()
                            speed_counter_text = fps_font.render(
                                f"{speed * 100:.0f}%", 1, (255, 255, 255))
                            SCREEN.blit(speed_counter_text,
                                        (speed_left, speed_top))
                        else:
                            paused = 0
                            speed = speeds[speed_index]
                            panel.set_played_button()
                            panel.display()
                            speed_counter_text = fps_font.render(
                                f"{speed * 100:.0f}%", 1, (255, 255, 255))
                            SCREEN.blit(speed_counter_text,
                                        (speed_left, speed_top))

                    if (panel.get_save_button().is_hovered(pos)):
                        path_save = "Saves/" + \
                            str(map.get_name_user()) + ".q5"
                        with open(path_save, 'wb') as f1:
                            pickle.dump(map, f1)
                        current_time = datetime.now().strftime("%H:%M:%S")

                if zoom_update > 0:
                    if event.button == 4:
                        if zoom < 1.7:
                            zoom += 0.05
                            map.handle_zoom(1)
                            panel.display()
                            speed_counter_text = fps_font.render(
                                f"{speed * 100:.0f}%", 1, (255, 255, 255))
                            SCREEN.blit(speed_counter_text,
                                        (speed_left, speed_top))
                    if event.button == 5:
                        if zoom > 0.8:
                            zoom -= 0.05
                            map.handle_zoom(0)
                            panel.display()
                            speed_counter_text = fps_font.render(
                                f"{speed * 100:.0f}%", 1, (255, 255, 255))
                            SCREEN.blit(speed_counter_text,
                                        (speed_left, speed_top))
                    zoom_update = 0

            if event.type == pygame.MOUSEBUTTONUP:
                if selection["is_active"]:
                    for i in selection["cells"]:
                        selected_cell = map.get_cell(i[0], i[1])
                        if map.get_shoveled():
                            selected_cell.clear()
                            selected_cell.display_around_shovel()
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
                                    if (39 >= x+k >= 0 and 39 >= y+j >= 0):
                                        map.get_cell(i[0]+k, i[1]+j).display()
                        else:
                            selected_cell.display()
                    map.buildings.sort(key=lambda i: (i.x, i.y))
                    print([(i.x, i.y) for i in map.buildings])
                    selection["cells"].clear()
                    selection["is_active"] = 0

            if event.type == pygame.MOUSEMOTION:
                # Display previous cell without hover
                if hovered_cell:
                    hovered_cell = map.get_cell(
                        hovered_coordinates[0], hovered_coordinates[1])
                    hovered_cell.display()
                    hovered_cell.display_around()
                if map.inMap(x, y) and pos[0] <= width_wo_panel and not selection["is_active"]:
                    hovered_coordinates = (x, y)
                    hovered_cell = map.get_cell(
                        hovered_coordinates[0], hovered_coordinates[1])
                    hovered_cell.handle_hover_button()
                    # hovered_cell.display_around()

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
                panel.get_up_button().handle_hover_button(pos, SCREEN)
                panel.get_down_button().handle_hover_button(pos, SCREEN)
                panel.get_pause_button().handle_hover_button(pos, SCREEN)
                panel.get_save_button().handle_hover_button(pos, SCREEN)

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    panel.set_window("none")
                    map.handle_esc()

                if pygame.key.get_pressed()[pygame.K_o]:
                    # outfile = open("Saves/test.plk",'wb')
                    # pickle.dump(map,outfile)
                    # outfile.close()
                    map.set_overlay("fire")

                if pygame.key.get_pressed()[pygame.K_p]:
                    volume = pygame.mixer.music.get_volume()
                    pygame.mixer.music.set_volume(volume + 0.05)
                    print("tunic", pygame.mixer.music.get_volume())
                    for i in map.sound_effect:
                        volume = map.sound_effect[i].get_volume()
                        map.sound_effect[i].set_volume(volume + 0.05)
                        print(map.sound_effect[i].get_volume(), i, "+")

                if pygame.key.get_pressed()[pygame.K_m]:
                    volume = pygame.mixer.music.get_volume()
                    pygame.mixer.music.set_volume(volume - 0.05)
                    print("tunic", pygame.mixer.music.get_volume())
                    for i in map.sound_effect:
                        volume = map.sound_effect[i].get_volume()
                        map.sound_effect[i].set_volume(volume - 0.05)
                        print(map.sound_effect[i].get_volume(), i, "-")

                # grid_button.handle_hover_button(pos, SCREEN)
                # home_button.handle_hover_button(pos, SCREEN)
                # shovel_button.handle_hover_button(pos, SCREEN)
                # road_button.handle_hover_button(pos, SCREEN)

        if map.get_overlay() in ("fire", "collapse"):
            map.display_overlay()

        walker_update_count += 1
        # print(walker_update_count)
        update_speed = 10 / (speed)
        if walker_update_count >= update_speed:
            # print(walker_update_count)
            map.update_walkers()
            panel.display()
            speed_counter_text = fps_font.render(
                f"{speed * 100:.0f}%", 1, (255, 255, 255))
            SCREEN.blit(speed_counter_text,
                        (speed_left, speed_top))
            # print("break")
            walker_update_count = 0

        fire_upadte_count += 1
        if fire_upadte_count >= update_speed:
            map.update_fire()
            map.update_collapse()
            fire_upadte_count = 0

        # if tmpbool :
        #     map.array[13][29] = Prefecture(13, 29, map.height_land, map.width_land,map.screen, map)
        #     SCREEN.blit(pygame.transform.scale(pygame.image.load("walker_sprites/test/Housng1a_00019.png"), (map.array[13][29].width, map.array[13][29].height)), (map.array[13][29].left, map.array[13][29].top))
        #     map.array[31][19] = EngineerPost(31, 19, map.height_land, map.width_land, map.screen, map)
        #     SCREEN.blit(pygame.transform.scale(pygame.image.load("walker_sprites/test/Housng1a_00019.png"), (map.array[31][19].width, map.array[31][19].height)), (map.array[31][19].left, map.array[31][19].top))
        #     tmpbool = 0
        clock.tick(60)
        fps = (int)(clock.get_fps())
        text_fps = fps_font.render(str(fps), 1, (255, 255, 255))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(
            0, HEIGH_SCREEN - text_fps.get_size()[1], 60, 40))
        SCREEN.blit(text_fps, (0, HEIGH_SCREEN - text_fps.get_size()[1]))

        pygame.display.flip()
