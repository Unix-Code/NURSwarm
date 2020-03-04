import pygame
import pygame.gfxdraw
import math
from pygame import Rect, Surface
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
        # clockwise rotation (in radians)
        self.angle = math.pi / 2
        self.pos: Vector = pos
        self.vel = vel
        self.BOT_RADIUS = 75
        self.WHEEL_WIDTH = 30
        self.WHEEL_DISTANCE_TO_CENTER = self.BOT_RADIUS + (self.WHEEL_WIDTH / 2)

    def update(self):
        self.pos = self.pos.add(self.vel)

    def rotate(self, pos: Vector, angle: int, is_clockwise: bool = True) -> None:
        vec_from_pos_to_center = self.pos.sub(pos)
        if is_clockwise:
            rotated_vec = vec_from_pos_to_center.rotated(angle)
            self.angle -= angle
        else:
            rotated_vec = vec_from_pos_to_center.rotated(-angle)
            self.angle += angle
        self.pos = pos.add(rotated_vec)

    def draw(self, display_surface) -> None:

        # bot radius
        BOT_RADIUS = 75
        SURFACE_WIDTH = SURFACE_HEIGHT = 200

        bot_surface = Surface((SURFACE_WIDTH, SURFACE_HEIGHT), pygame.SRCALPHA)

        # body of bot
        pygame.gfxdraw.aacircle(bot_surface, SURFACE_WIDTH // 2, SURFACE_HEIGHT // 2, BOT_RADIUS, GREEN)
        pygame.gfxdraw.filled_circle(bot_surface, SURFACE_WIDTH // 2 , SURFACE_HEIGHT // 2, BOT_RADIUS, GREEN)

        # axle
        AXLE_WIDTH = BOT_RADIUS * 2
        self.AXLE_WIDTH = AXLE_WIDTH
        AXLE_HEIGHT = 20
        AXLE_X = SURFACE_WIDTH // 2 - AXLE_WIDTH // 2
        AXLE_Y = SURFACE_HEIGHT // 2 - AXLE_HEIGHT // 2
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X , AXLE_Y, AXLE_WIDTH, AXLE_HEIGHT), LIGHT_PURPLE)

        # wheels
        WHEEL_WIDTH = 30
        WHEEL_Y = AXLE_Y - (WHEEL_WIDTH - AXLE_HEIGHT) // 2
        # left wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X - WHEEL_WIDTH, WHEEL_Y, WHEEL_WIDTH, WHEEL_WIDTH), RED)
        # right wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X + AXLE_WIDTH, WHEEL_Y, WHEEL_WIDTH, WHEEL_WIDTH), BLUE)

        bot_surface = pygame.transform.rotate(bot_surface, math.degrees(self.angle))

        draw_pos = self.pos.sub(Vector(bot_surface.get_width() // 2, bot_surface.get_height() // 2))

        display_surface.blit(bot_surface, draw_pos.coords())


clock = pygame.time.Clock()
angle = math.radians(1)
bot = Bot(Vector(WIDTH // 2, HEIGHT // 2), Vector(0, 0))

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

        bot.rotate(Vector(400, 310), angle, False)
        bot.update()
        bot.draw(display_surface)

        # refreshes entire window and surface object
        pygame.display.flip()
