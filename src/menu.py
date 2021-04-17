import sys

import pygame
from pygame.mixer import Sound

from button import Button


class Menu:
    """Overall class for a selection menu"""

    def __init__(self, main_path, options, caption, back=True, click=True):
        """Initialize the game, and create game resources"""

        pygame.init()

        # Back button?
        self.back = back

        # Clickable buttons? (except for Back button if present)
        self.click = click

        # Load game assets and data.
        self.path = main_path
        self.options = options

        # Are custom options for the buttons given?
        if type(self.options) is dict:
            self.custom = True
        else:
            self.custom = False
        self.texts = list(self.options.keys()) if self.custom else self.options
        self.click_sound = Sound(self.path + "sounds/click.wav")

        # Generate buttons and adequate screen width and height.
        self.buttons = []
        self.screen_height = 300 if len(self.texts) <= 3 else (len(self.texts) + 2) * 60
        self.screen_width = self._generate_buttons()
        self.screen_width = 400 if self.screen_width < 320 else self.screen_width + 80

        # Set screen.
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(caption)

    def _generate_buttons(self):
        """Make the buttons"""

        # List of widths of buttons.
        self.widths = []

        # Calculate position of first button.
        # As to make the list of buttons vertically centered on screen.
        n_options = len(self.texts)
        over = n_options // 2
        middle = n_options % 2
        ini_pos = (self.screen_height / 2) - 60 * over - 30 * (middle - 1)

        # Generate buttons.
        i = 0
        for option in self.texts:
            button = Button(
                msg=option,
                main_path=self.path,
                pos_y=ini_pos + (60 * i),
                **self.options[option] if self.custom else {}
            )
            i += 1
            self.buttons.append(button)
            self.widths.append(button.msg_image.get_width())

        # Add a back button if requested.
        if self.back:
            button = Button(
                msg="Back",
                main_path=self.path,
                pos_x=55,
                pos_y=35,
                t_size=25,
                b_height="auto",
                b_width=80,
                b_color=(255, 150, 70),
            )
            self.buttons.append(button)

        # Returns maximum width among the buttons.
        return max(self.widths)

    def run_menu(self):
        """Start the main loop for the menu"""
        while True:
            option_selected = self._check_events()
            self._update_screen()
            if option_selected:
                return option_selected

    def _check_events(self):
        """Check for option selected from menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.b_rect.collidepoint(event.pos):
                        if button.msg == "Back" or self.click:
                            self.click_sound.play()
                            return button.msg
                return None

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill((230, 230, 230))
        for button in self.buttons:
            button.draw_button(self.screen)
        pygame.display.flip()
