import pygame
from math import sqrt

WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
FPS = 60



#draw a rectangle with an opacity option 
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

pygame.display.set_caption("Quintus Caesar 3")

WIDTH, HEIGH = WIN.get_size()

#THIS PART IS FOR THE MAP GENERATION

land = pygame.image.load("game_screen/game_screen_sprites/land.png")
land_red_panel = pygame.image.load("game_screen/game_screen_sprites/land_red_panel.png")
land_blue_panel = pygame.image.load("game_screen/game_screen_sprites/land_blue_panel.png")
heigh_land = HEIGH/60
width_land = WIDTH*sqrt(2)/80
for i in range(40):
    for j in range(i):
        #quarter by quarter 
        if(i < 20):
            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)-width_land*j, HEIGH/6+i*heigh_land))
            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)+width_land*j, HEIGH/6+i*heigh_land))

            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)-width_land/2-width_land*j, HEIGH/6+i*heigh_land+heigh_land/2))
            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)+width_land/2+width_land*j, HEIGH/6+i*heigh_land+heigh_land/2))
        if(i >= 20 and j >= 20):
            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)-width_land*(j-20), (5*HEIGH/6-(i-19)*heigh_land)))
            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)+width_land*(j-20), 5*HEIGH/6-(i-19)*heigh_land))

            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)-width_land/2-width_land*(j-20), 5*HEIGH/6-(i-19)*heigh_land-heigh_land/2))
            WIN.blit(pygame.transform.scale(land, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)+width_land/2+width_land*(j-20), 5*HEIGH/6-(i-19)*heigh_land- heigh_land/2))

#WIN.blit(pygame.transform.scale(land_blue_panel, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)+width_land*10, HEIGH/6+11*heigh_land))
#WIN.blit(pygame.transform.scale(land_red_panel, (width_land, heigh_land)), ((WIDTH/2-WIDTH/12)-width_land*(j-20), (5*HEIGH/6-*heigh_land)))

#THIS PART IS FOR THE LEFT PANEL 

#background panel initialisation
panel_background = pygame.image.load("game_screen/game_screen_sprites/panel_background.png")
for i in range(2):
    for j in range(9):
        WIN.blit(pygame.transform.scale(panel_background, (WIDTH/24, HEIGH/10)), ((((i+22)/24)*WIDTH), (j/10)*HEIGH))
draw_rect_alpha(WIN, (50, 50, 50, 60), (WIDTH*(11/12), 0, WIDTH/12, HEIGH*9/10))

#panel overlays initialisation (on the top of the panel)
panel_overlays = pygame.image.load("game_screen/game_screen_sprites/paneling_overlays.png")
WIN.blit(pygame.transform.scale(panel_overlays, (WIDTH/18, HEIGH/36)), (11*WIDTH/12+5, HEIGH/32+2))


#white rectangle under the button on the panel
draw_rect_alpha(WIN, (255,255,255, 127), (177*WIDTH/192-2, 0.25*HEIGH-2, (WIDTH)/48+4, (HEIGH)/40+4))
draw_rect_alpha(WIN, (255,255,255, 127), (182*WIDTH/192-2, 0.25*HEIGH-2, (WIDTH)/48+4, (HEIGH)/40+4))
draw_rect_alpha(WIN, (255,255,255, 127), (187*WIDTH/192-2, 0.25*HEIGH-2, (WIDTH)/48+4, (HEIGH)/40+4))

#window upside button initialisation
panel_window_home = pygame.image.load("game_screen/game_screen_sprites/panel_window_home.png")
WIN.blit(pygame.transform.scale(panel_window_home, (WIDTH/12-10, HEIGH/17)), (11*WIDTH/12+5, 0.18*HEIGH))


#panel home button initialisation
panel_home_button = pygame.image.load("game_screen/game_screen_sprites/paneling_home_button.png")

WIN.blit(pygame.transform.scale(panel_home_button, (WIDTH/48, HEIGH/40)), (177*WIDTH/192, 0.25*HEIGH))

#panel shovel button initialisation
panel_shovel_button = pygame.image.load("game_screen/game_screen_sprites/paneling_shovel_button.png")
WIN.blit(pygame.transform.scale(panel_shovel_button, (WIDTH/48, HEIGH/40)), (182*WIDTH/192, 0.25*HEIGH))

#panel road button initialisation
panel_road_button = pygame.image.load("game_screen/game_screen_sprites/paneling_road_button.png")
WIN.blit(pygame.transform.scale(panel_road_button, (WIDTH/48, HEIGH/40)), (187*WIDTH/192, 0.25*HEIGH))

#panel information initialisation
draw_rect_alpha(WIN, (25, 25, 25, 127), (WIDTH*(11/12)+2, HEIGH*(8/17), WIDTH/12-4, 3*HEIGH/7-2))

#bottom panel initialisation
panel_bottom = pygame.image.load("game_screen/game_screen_sprites/paneling_bot.png")
WIN.blit(pygame.transform.scale(panel_bottom, (WIDTH/12, HEIGH/10)), (((11/12)*WIDTH), (0.9*HEIGH)))


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)
        pygame.display.flip()    

    pygame.quit()

