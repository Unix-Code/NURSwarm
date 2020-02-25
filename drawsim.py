import pygame
import pygame.gfxdraw
from pygame.locals import Rect

# activate/initiate the pygame library
num_pass, num_failed = pygame.init()
print(f"{num_pass} pygame modules succesfully initialized and {num_failed} failed.")

# RGB color constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_PURPLE = (50, 50, 128)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# background width and height
WIDTH = 400
HEIGHT = 800

# create the display surface object of specific dimension. (WIDTH,HEIGHT).
display_surface: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))

# set the pygame window name
pygame.display.set_caption("Basic Simulation")

# set the background color
display_surface.fill(GREY)

# bot radius
BOT_RADIUS = 150

# body of bot
pygame.gfxdraw.aacircle(display_surface, WIDTH // 2, HEIGHT // 2, BOT_RADIUS // 2, GREEN)
pygame.gfxdraw.filled_circle(display_surface, WIDTH // 2, HEIGHT // 2, BOT_RADIUS // 2, GREEN)

# axle
AXLE_WIDTH = 150
AXLE_HEIGHT = 20
AXLE_X = WIDTH // 2 - AXLE_WIDTH // 2
AXLE_Y = HEIGHT // 2 - AXLE_HEIGHT // 2
pygame.gfxdraw.box(display_surface, Rect(AXLE_X, AXLE_Y, AXLE_WIDTH, AXLE_HEIGHT), LIGHT_PURPLE)

# wheels
WHEEL_RADIUS = 30
WHEEL_Y = AXLE_Y - (WHEEL_RADIUS - AXLE_HEIGHT) // 2
# left wheel
pygame.gfxdraw.box(display_surface, Rect(AXLE_X - WHEEL_RADIUS // 2, WHEEL_Y, WHEEL_RADIUS, WHEEL_RADIUS), BLACK)
# right wheel
pygame.gfxdraw.box(display_surface, Rect(AXLE_X * 2 + WHEEL_RADIUS // 2, WHEEL_Y, WHEEL_RADIUS, WHEEL_RADIUS), BLACK)

clock = pygame.time.Clock()

# infinite loop
while True:
    clock.tick(60)
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quit the pygame and program.
        if event.type == pygame.QUIT:

            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

    # Refreshes entire window and surface object.
    pygame.display.flip()
    # move forward
    display_surface.scroll(0, -1)
