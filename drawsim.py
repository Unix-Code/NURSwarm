import pygame
import pygame.gfxdraw
import math
from pygame import Rect, Surface
from typing import Tuple
from utils import Vector

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

    def __init__(self, pos, vel):
        # self.draw()
        # self.rect = self.image.get_rect(center=(x, y))
        
        # clockwise rotation (in radians)
        self.angle = 0
        self.pos = pos
        self.vel = vel

    def update(self):
        self.pos = self.pos.add(self.vel)
        # self.rect = Rect()

    def draw(self) -> None:
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
        BOT_RADIUS = 75
        SURFACE_WIDTH = SURFACE_HEIGHT = 350

        bot_surface = Surface((SURFACE_WIDTH, SURFACE_HEIGHT), pygame.SRCALPHA)
        self.image = bot_surface

        # body of bot
        pygame.gfxdraw.aacircle(bot_surface, SURFACE_WIDTH // 2 + offset, SURFACE_HEIGHT // 2, BOT_RADIUS, GREEN)
        pygame.gfxdraw.filled_circle(bot_surface, SURFACE_WIDTH // 2 + offset, SURFACE_HEIGHT // 2, BOT_RADIUS, GREEN)

        # axle
        AXLE_WIDTH = BOT_RADIUS * 2
        self.AXLE_WIDTH = AXLE_WIDTH
        AXLE_HEIGHT = 20
        AXLE_X = SURFACE_WIDTH // 2 - AXLE_WIDTH // 2
        AXLE_Y = SURFACE_HEIGHT // 2 - AXLE_HEIGHT // 2
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X + offset, AXLE_Y, AXLE_WIDTH, AXLE_HEIGHT), LIGHT_PURPLE)

        # wheels
        WHEEL_WIDTH = 30
        WHEEL_Y = AXLE_Y - (WHEEL_WIDTH - AXLE_HEIGHT) // 2
        # left wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X - WHEEL_WIDTH + offset, WHEEL_Y, WHEEL_WIDTH, WHEEL_WIDTH), RED)
        # right wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X + AXLE_WIDTH + offset, WHEEL_Y, WHEEL_WIDTH, WHEEL_WIDTH), BLUE)

    def _get_left_wheel_vector(self) -> Vector:
        """Returns the relative vector from the center to the left wheel
        """
        left_wheel_angle = self.angle + math.pi / 2
        left_wheel_distance = BOT_RADIUS + (WHEEL_WIDTH / 2)
        return Vector.from_polar(left_wheel_distance, left_wheel_angle)
    
    def _get_left_wheel_pos_vector(self) -> Vector:
        return self.pos.add(self._get_left_wheel_vector())

    def _get_right_wheel_vector(self) -> Vector:
        """Returns the relative vector from the center to the right wheel
        """
        right_wheel_angle = self.angle - math.pi / 2
        right_wheel_distance = BOT_RADIUS + (WHEEL_WIDTH / 2)
        return Vector.from_polar(right_wheel_distance, right_wheel_angle)
    
    def _get_right_wheel_pos_vector(self) -> Vector:
        return self.pos.add(self._get_right_wheel_vector())

    def rotate_around_left_wheel(self, angle):
        left_wheel_pos = self._get_left_wheel_pos_vector()
        self.angle += angle
        offset = self._get_left_wheel_vector().invert()
        self.pos = left_wheel_pos.add(offset)

    def rotate_around_right_wheel(self, angle):
        right_wheel_pos = self._get_right_wheel_pos_vector()
        self.angle += angle
        offset = self._get_right_wheel_vector().invert()
        self.pos = right_wheel_pos.add(offset)

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
        print(center)

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

ticks = 0

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
        image, rect = bot.rotated_around_center(0)        

        # move forward
        bot.move_forward(1)

        # rotate image
        angle += 1
        image, rect = bot.rotated_around_center(angle)

        # draw the bot onto the backround surface
        display_surface.blit(image, rect)

        # refreshes entire window and surface object
        pygame.display.flip()

        ticks += 1
