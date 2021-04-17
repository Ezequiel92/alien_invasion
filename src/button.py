import pygame.font


class Button:
    """A class to represent a button on the screen"""

    def __init__(
        self,
        msg,
        main_path,
        font="bpmono",
        pos_x=None,
        pos_y=None,
        t_size=35,
        t_color=(0, 0, 0),
        b_height=50,
        b_width=260,
        b_color=(255, 175, 0),
    ):

        # Set the dimensions and properties of the text.
        self.msg = msg
        self.font_filename = f"{main_path}fonts/{font}.ttf"
        self.t_color = t_color
        self.font = pygame.font.Font(self.font_filename, t_size)

        # Set the dimensions and properties of the button.
        self.width = b_width
        self.height = b_height
        self.b_color = b_color

        # Set button vertical and horizontal position.
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Set the message.
        self._prep_msg()

        # Build the button's rect object.
        self.b_rect = pygame.Rect(0, 0, self.width, self.height)

    def _prep_msg(self):
        """Turn message into a rendered image and center text on the button"""
        self.msg_image = self.font.render(self.msg, True, self.t_color, self.b_color)
        self.msg_image_rect = self.msg_image.get_rect()
        if self.width == "auto":
            self.width = self.msg_image_rect.w + 40
        if self.height == "auto":
            self.height = self.msg_image_rect.h + 10

    def draw_button(self, draw_screen):
        """Draw button and message. By default the button is in the center of the screen"""
        if self.pos_x:
            self.b_rect.centerx = self.pos_x
        else:
            self.b_rect.centerx = draw_screen.get_rect().centerx
        if self.pos_y:
            self.b_rect.centery = self.pos_y
        else:
            self.b_rect.centery = draw_screen.get_rect().centery
        self.msg_image_rect.center = self.b_rect.center

        # Draw button.
        draw_screen.fill(self.b_color, self.b_rect)

        # Draw text.
        draw_screen.blit(self.msg_image, self.msg_image_rect)
