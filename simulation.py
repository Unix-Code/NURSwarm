import pygame
from pygame.locals import *
import pygame.gfxdraw
from utils import *
from random import randint
from flock import flock

class Bot(pygame.sprite.Sprite):
    def __init__(self, velocity, pos, size, id):
        pygame.sprite.Sprite.__init__(self)
        BOT_IMG = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(BOT_IMG, int(size/2), int(size/2), int(size/2 - 1), (0, 255, 0))
        pygame.gfxdraw.filled_circle(BOT_IMG, int(size/2), int(size/2), int(size/2 - 1), (0, 255, 0))
        self.image = BOT_IMG
        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.velocity = velocity
        self.pos = pos
        self.size = size
        self.id = id

    def update(self, swarm_bots, nearby_bots, dest_vector):
        newpos = self.calcnewpos(self.rect, swarm_bots, nearby_bots, dest_vector)
        self.rect = newpos

    def calcnewpos(self, rect, swarm_bots, nearby_bots, dest_vector):
        accel = flock(swarm_bots, nearby_bots, dest_vector, self.velocity)
        self.velocity = self.velocity.add(accel)
        MAX_SPEED = self.velocity.MAX_SPEED
        self.velocity = self.velocity.limit(MAX_SPEED) if self.velocity.speed > MAX_SPEED else self.velocity
        self.pos = self.pos.add(self.velocity)
        self.pos.speed = 0 # Keep Speed 0 cuz why not
        rect.x, rect.y = self.pos.x, self.pos.y
        return rect

    def out_of_bounds(self, max_width, max_height):
        tolerance = 5 # pre-emptive collision
        x, y = self.pos.add(self.velocity).coords()
        return (x + self.size / 2 > max_width + tolerance
            or y + self.size / 2 > max_height + tolerance
            or x - self.size / 2 < 0 - tolerance
            or y - self.size / 2 < 0 - tolerance)


pygame.init()

size = width, height = 800, 800
black = 0, 0, 0

screen = pygame.display.set_mode(size)

BOT_SIZE = 10
SWARM_SIZE = 50
CURR_BOT_ID = 0

bots = []

def generate_bot():
    global CURR_BOT_ID
    CURR_BOT_ID += 1
    rand_x = randint(BOT_SIZE, width - BOT_SIZE)
    rand_y = randint(BOT_SIZE, height - BOT_SIZE)
    rand_vel_x = randint(-5, 5)
    rand_vel_y = randint(-5, 5)
    rand_vel_speed = euclid_distance((rand_x, rand_y), (rand_x + rand_vel_x, rand_y + rand_vel_y))
    return Bot(Vector(rand_vel_x, rand_vel_y, rand_vel_speed), Vector(rand_x, rand_y, 0), BOT_SIZE, CURR_BOT_ID)

def get_nearby_bots(bots, bot, tolerance):
    nearby_bots = [other_bot.pos.sub(bot.pos)
        for other_bot in bots
        if euclid_distance(bot.pos.coords(), other_bot.pos.coords()) < tolerance
        and euclid_distance(bot.pos.coords(), other_bot.pos.coords()) != 0]
    return nearby_bots

for i in range(0, SWARM_SIZE):
    bots.append(generate_bot())

clock = pygame.time.Clock()

game_over = False
while not game_over:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_over = True

    goal = pygame.mouse.get_pos()
    goal = Vector(goal[0], goal[1], 0)

    screen.fill(black)
    for bot in bots:
        #print("ID: %d -- Velocity: (%f, %f)" % (bot.id, bot.velocity.x, bot.velocity.y))
        #print("ID: %d -- Position: (%f, %f)" % (bot.id, bot.pos.x, bot.pos.y))
        bot.update([swarm_bot.velocity for swarm_bot in bots], get_nearby_bots(bots, bot, 100),
         goal.sub(bot.pos) if euclid_distance(goal.coords(), bot.pos.coords()) < 0.5 * width else None)
        #if (bot.out_of_bounds(width, height)):
        #    bot.velocity = bot.velocity.invert()
    bots = list(filter(lambda b: not b.out_of_bounds(width, height), bots))

    if len(bots) < SWARM_SIZE:
        for i in range(0, SWARM_SIZE - len(bots)):
            bots.append(generate_bot())

    for bot in bots:
        screen.blit(bot.image, bot.rect)

    pygame.display.flip()
