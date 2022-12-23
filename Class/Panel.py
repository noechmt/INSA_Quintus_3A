import pygame
from Class.Button import Button


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


class Panel():
    def __init__(self, screen):
        self.screen = screen
        self.width_screen, self.height_screen = self.screen.get_size()
        self.init_sprites()
        self.init_buttons()
        self.window_current = self.window_home
        self.display()
        pass

    def init_sprites(self):
        self.background = pygame.image.load(
            "game_screen/game_screen_sprites/panel_background.png")
        self.overlays = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_overlays.png")
        self.window_home = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_home.png")
        self.window_road = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_road.png")
        self.grid_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_grid_button.png")
        self.home_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_home_button.png")
        self.shovel_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_shovel_button.png")
        self.road_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_road_button.png")
        self.bottom = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_bot.png")

    def init_buttons(self):
        self.grid_button = Button(177*self.width_screen/192, 0.125*self.height_screen,
                                  self.width_screen/48, self.height_screen / 40, self.grid_button_sprite)
        self.home_button = Button(177*self.width_screen/192, 0.25*self.height_screen,
                                  self.width_screen/48, self.height_screen/40, self.home_button_sprite)
        self.shovel_button = Button(182*self.width_screen/192, 0.25*self.height_screen,
                                    self.width_screen/48, self.height_screen/40, self.shovel_button_sprite)
        self.road_button = Button(187*self.width_screen/192, 0.25*self.height_screen,
                                  self.width_screen/48, self.height_screen/40, self.road_button_sprite)

    def display(self):
        for i in range(2):
            for j in range(9):
                self.screen.blit(pygame.transform.scale(self.background, (self.width_screen/24,
                                                                          self.height_screen/10)), ((((i+22)/24)*self.width_screen), (j/10)*self.height_screen))
        draw_rect_alpha(self.screen, (50, 50, 50, 60), (self.width_screen *
                                                        (11/12), 0, self.width_screen/12, self.height_screen*9/10))
        self.screen.blit(pygame.transform.scale(self.overlays, (self.width_screen/18,
                                                                self.height_screen/36)), (11*self.width_screen/12+5, self.height_screen/32+2))

        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192-2,
                        0.25*self.height_screen-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (182*self.width_screen/192-2,
                        0.25*self.height_screen-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (187*self.width_screen/192-2,
                        0.25*self.height_screen-2, (self.width_screen)/48+4, (self.height_screen)/40+4))

        self.screen.blit(pygame.transform.scale(self.window_current, (self.width_screen /
                                                                      12-10, self.height_screen/17)), (11*self.width_screen/12+5, 0.18*self.height_screen))

        self.grid_button.draw(self.screen)

        self.home_button.draw(self.screen)

        self.shovel_button.draw(self.screen)

        self.road_button.draw(self.screen)

        draw_rect_alpha(self.screen, (25, 25, 25, 127), (self.width_screen*(11/12)+2,
                        self.height_screen*(8/17), self.width_screen/12-4, 3*self.height_screen/7-2))

        self.screen.blit(pygame.transform.scale(self.bottom, (self.width_screen/12,
                                                              self.height_screen/10)), (((11/12)*self.width_screen), (0.9*self.height_screen)))

    def set_window(self, choice):
        if choice == "road":
            self.window_current = self.window_road
        if choice == "home":
            self.window_current = self.window_home
        self.screen.blit(pygame.transform.scale(self.window_current, (self.width_screen /
                                                                      12-10, self.height_screen/17)), (11*self.width_screen/12+5, 0.18*self.height_screen))

    def get_grid_button(self):
        return self.grid_button

    def get_home_button(self):
        return self.home_button

    def get_shovel_button(self):
        return self.shovel_button

    def get_grid_button(self):
        return self.grid_button

    def get_road_button(self):
        return self.road_button