from turtle import title
from numpy import choose
import pygame

from GUI.Button import Button
from GUI.choose_name import choose_name


def title_screen():

    pygame.init()

    # Create screen variable and set the size of the screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Get the size of the user's screen
    width_screen, height_screen = screen.get_size()

    # Set the caption of the window as Caesar III
    pygame.display.set_caption('Caesar III')

    # Load the picture and scale it to the full size
    background_image = pygame.image.load(
        "GUI/Images/Title screen/Background.png")
    screen.blit(pygame.transform.scale(
        background_image, (width_screen, height_screen)), (0, 0))

    # Create the rectangle for the menu
    (width_menu, height_menu) = (width_screen / 5, height_screen / 3)
    (left_menu, top_menu) = (2 * width_screen / 5, height_screen / 3)
    menu_background = pygame.image.load(
        "GUI/Images/Title screen/Menu_background.jpg")
    screen.blit(pygame.transform.scale(
        menu_background, (width_menu, height_menu)), (left_menu, top_menu))

    # We want to keep the ration of the logo so height is width/3 as in the original size
    width_logo = width_menu - 2 * width_screen / 60
    height_logo = width_logo / 3
    (left_logo, top_logo) = (left_menu +
                             width_screen / 60, top_menu + height_screen / 60)
    logo_menu = pygame.image.load(
        "GUI/Images/Title screen/Logo_menu.png")
    screen.blit(pygame.transform.scale(
        logo_menu, (width_logo, height_logo)), (left_logo, top_logo))

    logo_background = pygame.image.load(
        "GUI/Images/Title screen/Logo_background.jpg")

    width_buttons = width_logo
    height_buttons = height_logo // 2
    left_buttons = left_logo

    top_start_button = top_logo + height_logo + height_screen / 30
    start_game_button = Button(left_buttons, top_start_button, width_buttons,
                               height_buttons, image=logo_background, text="Commencez la partie")
    start_game_button.draw(screen)

    top_leave_button = top_logo + 2 * height_logo
    leave_game_button = Button(left_buttons, top_leave_button, width_buttons,
                               height_buttons, image=logo_background, text="Quittez le jeu")
    leave_game_button.draw(screen)

    # Display the window
    pygame.display.flip()

    # Loop that check if the user wants to close the window
    running = True
    window_name = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if leave_game_button.is_hovered(pos):
                    running = False
                if start_game_button.is_hovered(pos):
                    window_name = True
                    running = False
            if event.type == pygame.MOUSEMOTION:
                start_game_button.handle_hover_button(pos, screen)
                leave_game_button.handle_hover_button(pos, screen)

        # Set the FPS at 60
        clock.tick(60)

        # Update the screen
        pygame.display.flip()

    if window_name:
        # We display again this window if the back button is pressed from choose_name
        if (not choose_name()):
            title_screen()
