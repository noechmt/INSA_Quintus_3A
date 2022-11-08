import pygame
from math import sqrt

#draw a rectangle with an opacity option 
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def game_screen():
    SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    FPS = 60


    pygame.display.set_caption("Quintus Caesar 3")

    WIDTH_SCREEN, HEIGH_SCREEN = SCREEN.get_size()

    #THIS PART IS FOR THE MAP GENERATION

    land = pygame.image.load("game_screen/game_screen_sprites/land.png")
    land_red_panel = pygame.image.load("game_screen/game_screen_sprites/land_red_panel.png")
    land_blue_panel = pygame.image.load("game_screen/game_screen_sprites/land_blue_panel.png")
    heigh_land = HEIGH_SCREEN/60
    width_land = WIDTH_SCREEN*sqrt(2)/80
    for i in range(40):
        for j in range(i):
            #quarter by quarter 
            if(i < 20):
                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)-width_land*j, HEIGH_SCREEN/6+i*heigh_land))
                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)+width_land*j, HEIGH_SCREEN/6+i*heigh_land))

                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)-width_land/2-width_land*j, HEIGH_SCREEN/6+i*heigh_land+heigh_land/2))
                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)+width_land/2+width_land*j, HEIGH_SCREEN/6+i*heigh_land+heigh_land/2))
            if(i >= 20 and j >= 20):
                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)-width_land*(j-20), (5*HEIGH_SCREEN/6-(i-19)*heigh_land)))
                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)+width_land*(j-20), 5*HEIGH_SCREEN/6-(i-19)*heigh_land))

                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)-width_land/2-width_land*(j-20), 5*HEIGH_SCREEN/6-(i-19)*heigh_land-heigh_land/2))
                SCREEN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)+width_land/2+width_land*(j-20), 5*HEIGH_SCREEN/6-(i-19)*heigh_land- heigh_land/2))

    #SCREEN.blit(pygame.transform.scale(land_blue_panel, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)+width_land*10, HEIGH_SCREEN/6+11*heigh_land))
    #SCREEN.blit(pygame.transform.scale(land_red_panel, (width_land, heigh_land)), ((WIDTH_SCREEN/2-WIDTH_SCREEN/12)-width_land*(j-20), (5*HEIGH_SCREEN/6-*heigh_land)))

    #THIS PART IS FOR THE LEFT PANEL 

    #background panel initialisation
    panel_background = pygame.image.load("game_screen/game_screen_sprites/panel_background.png")
    for i in range(2):
        for j in range(9):
            SCREEN.blit(pygame.transform.scale(panel_background, (WIDTH_SCREEN/24, HEIGH_SCREEN/10)), ((((i+22)/24)*WIDTH_SCREEN), (j/10)*HEIGH_SCREEN))
    draw_rect_alpha(SCREEN, (50, 50, 50, 60), (WIDTH_SCREEN*(11/12), 0, WIDTH_SCREEN/12, HEIGH_SCREEN*9/10))

    #panel overlays initialisation (on the top of the panel)
    panel_overlays = pygame.image.load("game_screen/game_screen_sprites/paneling_overlays.png")
    SCREEN.blit(pygame.transform.scale(panel_overlays, (WIDTH_SCREEN/18, HEIGH_SCREEN/36)), (11*WIDTH_SCREEN/12+5, HEIGH_SCREEN/32+2))


    #white rectangle under the button on the panel
    draw_rect_alpha(SCREEN, (255,255,255, 127), (177*WIDTH_SCREEN/192-2, 0.25*HEIGH_SCREEN-2, (WIDTH_SCREEN)/48+4, (HEIGH_SCREEN)/40+4))
    draw_rect_alpha(SCREEN, (255,255,255, 127), (182*WIDTH_SCREEN/192-2, 0.25*HEIGH_SCREEN-2, (WIDTH_SCREEN)/48+4, (HEIGH_SCREEN)/40+4))
    draw_rect_alpha(SCREEN, (255,255,255, 127), (187*WIDTH_SCREEN/192-2, 0.25*HEIGH_SCREEN-2, (WIDTH_SCREEN)/48+4, (HEIGH_SCREEN)/40+4))

    #SCREENdow upside button initialisation
    panel_window_home = pygame.image.load("game_screen/game_screen_sprites/panel_window_home.png")
    SCREEN.blit(pygame.transform.scale(panel_window_home, (WIDTH_SCREEN/12-10, HEIGH_SCREEN/17)), (11*WIDTH_SCREEN/12+5, 0.18*HEIGH_SCREEN))


    #panel home button initialisation
    panel_home_button = pygame.image.load("game_screen/game_screen_sprites/paneling_home_button.png")

    SCREEN.blit(pygame.transform.scale(panel_home_button, (WIDTH_SCREEN/48, HEIGH_SCREEN/40)), (177*WIDTH_SCREEN/192, 0.25*HEIGH_SCREEN))

    #panel shovel button initialisation
    panel_shovel_button = pygame.image.load("game_screen/game_screen_sprites/paneling_shovel_button.png")
    SCREEN.blit(pygame.transform.scale(panel_shovel_button, (WIDTH_SCREEN/48, HEIGH_SCREEN/40)), (182*WIDTH_SCREEN/192, 0.25*HEIGH_SCREEN))

    #panel road button initialisation
    panel_road_button = pygame.image.load("game_screen/game_screen_sprites/paneling_road_button.png")
    SCREEN.blit(pygame.transform.scale(panel_road_button, (WIDTH_SCREEN/48, HEIGH_SCREEN/40)), (187*WIDTH_SCREEN/192, 0.25*HEIGH_SCREEN))

    #panel information initialisation
    draw_rect_alpha(SCREEN, (25, 25, 25, 127), (WIDTH_SCREEN*(11/12)+2, HEIGH_SCREEN*(8/17), WIDTH_SCREEN/12-4, 3*HEIGH_SCREEN/7-2))

    #bottom panel initialisation
    panel_bottom = pygame.image.load("game_screen/game_screen_sprites/paneling_bot.png")
    SCREEN.blit(pygame.transform.scale(panel_bottom, (WIDTH_SCREEN/12, HEIGH_SCREEN/10)), (((11/12)*WIDTH_SCREEN), (0.9*HEIGH_SCREEN)))



    run = True
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)
        pygame.display.flip()    

