import pygame
import pygame.gfxdraw
from pygame import Rect, Surface
from typing import Tuple

# activate/initiate the pygame library
num_pass, num_failed = pygame.init()
print(f"{num_pass} pygame modules succesfully initialized and {num_failed} failed.")

# RGB color constants
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)
LIGHT_PURPLE = (50, 50, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# background width and height
WIDTH = 800
HEIGHT = 800

# set the pygame window name
pygame.display.set_caption("Basic Simulation")

# create the display surface object of specific dimension. (WIDTH,HEIGHT).
display_surface: Surface = pygame.display.set_mode((WIDTH, HEIGHT))

# set the background color
display_surface.fill(WHITE)


class Bot:
    """A drawing of bot which can be manipulated."""

    def __init__(self):
        self.draw()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def draw(self, offset: int = 0) -> None:
        """Renders the actual bot image.

        Consists of two square wheels, a rectangular axle connected the wheels,
        and a circular base.

        Parameters
        ----------
        offset : int
            The number of pixels to shift the drawing of the bot
            relative to the base surface.
        """

        # bot radius
        BOT_RADIUS = 150
        SURFACE_WIDTH = SURFACE_HEIGHT = 350

        bot_surface = Surface((SURFACE_WIDTH, SURFACE_HEIGHT), pygame.SRCALPHA)
        self.image = bot_surface

        # body of bot
        pygame.gfxdraw.aacircle(bot_surface, SURFACE_WIDTH // 2 + offset, SURFACE_HEIGHT // 2, BOT_RADIUS // 2, GREEN)
        pygame.gfxdraw.filled_circle(bot_surface, SURFACE_WIDTH // 2 + offset, SURFACE_HEIGHT // 2, BOT_RADIUS // 2, GREEN)

        # axle
        AXLE_WIDTH = 150
        self.AXLE_WIDTH = AXLE_WIDTH
        AXLE_HEIGHT = 20
        AXLE_X = SURFACE_WIDTH // 2 - AXLE_WIDTH // 2
        AXLE_Y = SURFACE_HEIGHT // 2 - AXLE_HEIGHT // 2
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X + offset, AXLE_Y, AXLE_WIDTH, AXLE_HEIGHT), LIGHT_PURPLE)

        # wheels
        WHEEL_RADIUS = 30
        WHEEL_Y = AXLE_Y - (WHEEL_RADIUS - AXLE_HEIGHT) // 2
        # left wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X - WHEEL_RADIUS // 2 + offset, WHEEL_Y, WHEEL_RADIUS, WHEEL_RADIUS), RED)
        # right wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X + AXLE_WIDTH - WHEEL_RADIUS // 2 + offset, WHEEL_Y, WHEEL_RADIUS, WHEEL_RADIUS), BLUE)

    def rotated_around_center(self, angle: int) -> Tuple[Surface, Rect]:
        """Returns a new instance of the surface and rectangle after rotating
        the bot counter-clockwise around its center by the given angle.

        Parameters
        ----------
        angle : int
            The degrees to rotate the bot counter-clockwise by.

        Returns
        ----------
        A tuple consisting of the new surface and rectangle after
        the bot has been rotated.
        """

        center = self.rect.center
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=center)

        return rotated_image, new_rect

    def rotated_around_left_wheel(self, angle: int) -> Tuple[Surface, Rect]:
        """Returns a new instance of the surface and rectangle after rotating
        the bot counter-clockwise around its left wheel by the given angle.

        Parameters
        ----------
        angle : int
            The degrees to rotate the bot counter-clockwise by.

        Returns
        ----------
        A tuple consisting of the new surface and rectangle after
        the bot has been rotated.
        """

        self.draw(self.AXLE_WIDTH // 2)
        center = self.rect.center
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=center)

        return rotated_image, new_rect

    def rotated_around_right_wheel(self, angle: int) -> Tuple[Surface, Rect]:
        """Returns a new instance of the surface and rectangle after rotating
        the bot counter-clockwise around its right wheel by the given angle.

        Parameters
        ----------
        angle : int
            The degrees to rotate the bot counter-clockwise by.

        Returns
        ----------
        A tuple consisting of the new surface and rectangle after
        the bot has been rotated.
        """

        self.draw(-self.AXLE_WIDTH // 2)
        center = self.rect.center
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=center)

        return rotated_image, new_rect

    def move_forward(self, pixels: int) -> None:
        """Moves the bot forward by the given amount of pixels.

        Parameters
        ----------
        pixels : int
            The amount of pixels to move the bot forward by
        """

        self.rect.move_ip(0, -pixels)


clock = pygame.time.Clock()
angle = 0
bot = Bot()

if __name__ == "__main__":
    # start the program
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

        # fill in the background to hide past drawings
        display_surface.fill(WHITE)

        # move forward
        bot.move_forward(1)

        # rotate image
        angle += 1
        image, rect = bot.rotated_around_center(angle)

        # draw the bot onto the backround surface
        display_surface.blit(image, rect)

        # refreshes entire window and surface object
        pygame.display.flip()
