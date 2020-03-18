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
    """A drawing of bot which can be manipulated.

    Attributes
    ----------
    angle : `float`
        Angle in radians of the bot (using the unit-circle)
    pos : `Vector`
        The position of the bot's center as a Vector.
    vel : `Vector`
        The bot's current velocity.
    BOT_RADIUS: `int`
        The radius of the bot's body (which is a circle)
    WHEEL_WIDTH: `int`
        The entire width of the bot's wheel (which is a rectangle)
    """
    # bot radius
    BOT_RADIUS = 75
    SURFACE_WIDTH = SURFACE_HEIGHT = 200

    AXLE_WIDTH = BOT_RADIUS * 2
    AXLE_HEIGHT = 20
    # wheels
    WHEEL_WIDTH = 30
    WHEEL_DISTANCE = WHEEL_WIDTH / 2 + BOT_RADIUS

    def __init__(self, pos: Vector, vel: Vector):
        self.angle: float = math.pi / 2
        self.pos: Vector = pos
        self.vel: Vector = vel

    def update(self):
        self.pos = self.pos.add(self.vel)

    def rotate(self, pos: Vector, angle: float, is_clockwise: bool = True) -> None:
        """Rotates the bot around the given position by the given angle
        either clockwise or counter-clockwise.

        Parameters
        ------------
        pos: `Vector`
            The position to rotate the bot around.
        angle: `float`
            The angle given in radians to rotate the bot by.
        is_clockwise: `bool`
            Whether to rotate the bot clockwise or counter-clockwise.
        """

        vec_from_pos_to_center = self.pos.sub(pos)
        if is_clockwise:
            angle = -angle
        rotated_vec = vec_from_pos_to_center.rotated(angle)
        self.angle += angle
        self.pos = pos.add(rotated_vec)

    def turn_on_right_wheel(self, angle: float) -> None:
        """Rotates the bot clockwise around the right wheel by the given angle.

        Parameters
        ------------
        angle: `float`
            The angle given in radians to rotate the bot by.
        """
        right_wheel_heading = self.angle - math.pi / 2
        right_wheel_pos: Vector = self.pos.add(Vector.from_polar(Bot.WHEEL_DISTANCE, right_wheel_heading))
        bot.rotate(right_wheel_pos, angle, True)

    def turn_on_left_wheel(self, angle: float) -> None:
        """Rotates the bot counter-clockwise around the left wheel by the given angle.

        Parameters
        ------------
        angle: `float`
            The angle given in radians to rotate the bot by.
        """
        left_wheel_heading = self.angle + math.pi / 2
        left_wheel_pos: Vector = self.pos.add(Vector.from_polar(Bot.WHEEL_DISTANCE, left_wheel_heading))
        bot.rotate(left_wheel_pos, angle, False)

    def draw(self, display_surface: Surface) -> None:
        """Renders the bot at it's current angle and position on the given surface."""

        # bot radius

        bot_surface = Surface((Bot.SURFACE_WIDTH, Bot.SURFACE_HEIGHT), pygame.SRCALPHA)

        # body of bot
        pygame.gfxdraw.aacircle(bot_surface, Bot.SURFACE_WIDTH // 2, Bot.SURFACE_HEIGHT // 2, Bot.BOT_RADIUS, GREEN)
        pygame.gfxdraw.filled_circle(bot_surface, Bot.SURFACE_WIDTH // 2 , Bot.SURFACE_HEIGHT // 2, Bot.BOT_RADIUS, GREEN)

        # axle
        AXLE_X = Bot.SURFACE_WIDTH / 2 - Bot.AXLE_WIDTH / 2
        AXLE_Y = Bot.SURFACE_HEIGHT / 2 - Bot.AXLE_HEIGHT / 2
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X , AXLE_Y, Bot.AXLE_WIDTH, Bot.AXLE_HEIGHT), LIGHT_PURPLE)

        # wheels
        WHEEL_Y = AXLE_Y - (Bot.WHEEL_WIDTH - Bot.AXLE_HEIGHT) / 2
        # left wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X - Bot.WHEEL_WIDTH, WHEEL_Y, Bot.WHEEL_WIDTH, Bot.WHEEL_WIDTH), RED)
        # right wheel
        pygame.gfxdraw.box(bot_surface, Rect(AXLE_X + Bot.AXLE_WIDTH, WHEEL_Y, Bot.WHEEL_WIDTH, Bot.WHEEL_WIDTH), BLUE)

        bot_surface = pygame.transform.rotate(bot_surface, math.degrees(self.angle - math.pi / 2))

        # invert the y-axis
        draw_pos = self.pos.sub(Vector(bot_surface.get_width() / 2, -bot_surface.get_height() / 2))

        draw_pos = Vector(draw_pos.x, HEIGHT - draw_pos.y)

        display_surface.blit(bot_surface, draw_pos.coords())


clock = pygame.time.Clock()
angle = math.radians(1)
bot = Bot(Vector(WIDTH // 2, HEIGHT // 2), Vector(0, 0))

tick_rate = 60
paused = False

if __name__ == "__main__":
    # start the program
    while True:
        clock.tick(tick_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()
            if event.type == pygame.KEYDOWN:
                # pause the game
                if event.key == pygame.K_p:
                    paused = not paused
                # speed up the simulation
                elif event.key == pygame.K_EQUALS:
                    tick_rate = min(tick_rate + 5, 60)
                # slow down the simulation
                elif event.key == pygame.K_MINUS:
                    tick_rate = max(tick_rate - 5, 5)

        if not paused:
            # fill in the background to hide past drawings
            display_surface.fill(WHITE)

            bot.turn_on_left_wheel(angle)
            bot.update()
            bot.draw(display_surface)

            # refreshes entire window and surface object
            pygame.display.flip()
