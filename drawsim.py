# import pygame module in this program 
import pygame
from pygame.locals import *
import pygame.gfxdraw

# activate the pygame library . 
# initiate pygame and give permission 
# to use pygame's functionality. 
pygame.init() 
  
# define the RGB value 
# for white, green, 
# blue, black, red 
# colour respectively. 
white = (255, 255, 255) 
green = (0, 255, 0) 
light_purple = (50, 50, 128)
black = (0, 0, 0) 
grey = (200, 200, 200)
# assigning values to X and Y variable 
X = 400
Y = 400
  
# create the display surface object 
# of specific dimension..e(X,Y). 
display_surface = pygame.display.set_mode((X, Y)) 
  
# # set the pygame window name 
# pygame.display.set_caption('Drawing') 
  
# completely fill the surface object  
# with white colour  
display_surface.fill(grey) 

# axle size
axle_width = 150
axle_height = 20

# wheel size
wheel_size = 30

# bot size
bot_size = 150

pygame.gfxdraw.aacircle(display_surface, int(X/2), int(Y/2), int(bot_size/2 - 1), green)
pygame.gfxdraw.filled_circle(display_surface, int(X/2), int(Y/2), int(bot_size/2 - 1), green)
pygame.gfxdraw.box(display_surface, Rect(X/2 - axle_width/2, Y/2 - axle_height/2, axle_width, axle_height), light_purple)
pygame.gfxdraw.box(display_surface, Rect(X/2 - axle_width/2 - wheel_size/2, Y/2 - axle_height/2 - (wheel_size - axle_height) / 2, wheel_size, wheel_size), black)
pygame.gfxdraw.box(display_surface, Rect(X/2 + axle_width/2 - wheel_size/2, Y/2 - axle_height/2 - (wheel_size - axle_height) / 2, wheel_size, wheel_size), black)
# pygame.gfxdraw.
  
# infinite loop 
while True : 
      
    # iterate over the list of Event objects 
    # that was returned by pygame.event.get() method. 
    for event in pygame.event.get() : 
  
        # if event object type is QUIT 
        # then quitting the pygame 
        # and program both. 
        if event.type == pygame.QUIT : 
  
            # deactivates the pygame library 
            pygame.quit() 
  
            # quit the program. 
            quit() 
  
        # Draws the surface object to the screen.  
        pygame.display.update()  