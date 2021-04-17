import sys

import pygame
from pygame.mixer import Sound

from button import Button


class InputBox:
    """Overall class to input new user"""

    def __init__(self, main_path, old_users):

        pygame.init()

        # List of already registered users.
        self.old_users = old_users

        # Display screen.
        self.screen = pygame.display.set_mode((500, 300))
        self.screen_rect = self.screen.get_rect()

        # Click sound.
        self.click_sound = Sound(main_path + "sounds/click.wav")

        # Fonts.
        self.font_filename = main_path + "fonts/bpmono.ttf"

        # Color and font constants.
        self.color_inactive = pygame.Color("gray60")
        self.color_active = pygame.Color("black")
        self.color_warning = pygame.Color("red")
        self.font = pygame.font.Font(self.font_filename, 20)
        self.font_warning = pygame.font.SysFont("calibri", 22)

        # Input box parameters.
        self.rect = pygame.Rect(0, 0, 140, 32)
        self.rect.center = (self.screen_rect.x, self.screen_rect.y)
        self.color = self.color_inactive

        # Text parameters.
        self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.txt_indication = self.font.render(
            "New user name:", True, self.color_active
        )

        # Logic flow variables.
        self.active = False
        self.warning = False
        self.new_user = None

        # Back button.
        self.button = Button(
            msg="Back",
            main_path=main_path,
            pos_x=55,
            pos_y=35,
            t_size=25,
            b_height=40,
            b_width=80,
            b_color=(255, 150, 70),
        )

    def run_menu(self):
        """Start the main loop for the menu"""
        while True:
            self.new_user = self._check_events()
            self._update_screen()
            if self.new_user in self.old_users:
                # If new user already exists, clean screen and set warning.
                self._resize()
                self._clean(self.new_user)
                self.new_user = None
            elif self.new_user:
                return self.new_user

    def _check_events(self):
        """Check input from user"""
        response = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.b_rect.collidepoint(event.pos):
                    self.click_sound.play()
                    response = "Back"
                elif self.rect.collidepoint(event.pos):
                    self.click_sound.play()
                    # Toggle the active state of input box.
                    self.active = not self.active
                else:
                    self.active = False
                # Set the correct color for the input box.
                self.color = self.color_active if self.active else self.color_inactive
            elif event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        # No leading or trailing whitespaces allowed.
                        response = self.text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = self.font.render(self.text, True, self.color)

        return response

    ########################################################################################
    # Screen functions.
    ########################################################################################

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self._resize()
        self.screen.fill((230, 230, 230))
        self._draw()
        pygame.display.flip()

    def _resize(self):
        """Resize the box if the text is too long"""
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.rect.center = self.screen.get_rect().center

    def _clean(self, user):
        """Clean screen and display warning if user already exist"""
        self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.warning = True
        self.txt_warning = self.font_warning.render(
            f"{user} already exist as an user.", True, self.color_warning
        )

    def _draw(self):
        """Draw elements on screen"""

        # Blit the user input text.
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Blit the indication text.
        self.screen.blit(self.txt_indication, (self.rect.x, self.rect.y - 30))
        if self.warning:
            self.screen.blit(self.txt_warning, (self.rect.x - 50, self.rect.y + 55))

        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

        # Draw back button.
        self.button.draw_button(self.screen)
