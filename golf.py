import random
import os
import pygame, sys
from pygame.locals import *
import argparse
import math

pygame.init()
frame_rate = pygame.time.Clock()

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)
DARKG = (0,100,0)
BROWN = (165,42,42)

#globals
WIDTH = 500
HEIGHT = 700
BALL_RADIUS = 10
BALL_POSITION = [200, 600]
SLOW_TIME = 100
HOLE_RADIUS = BALL_RADIUS + 5
HOLE_POSITION = [200, 50]

def total_distance(x, y, ball_position):
    return math.sqrt(math.pow(x - ball_position[0], 2) + math.pow(y - ball_position[1], 2))

def tg(x1, y1, x2, y2):
    sign_x = 1
    sign_y = 1

    if x1 < x2 and y1 < y2:
        sign_x = 1
        sign_y = 1
    if x1 < x2 and y1 > y2:
        sign_x = 1
        sign_y = -1
    if x1 > x2 and y1 < y2:
        sign_x = -1
        sign_y = 1
    if x1 > x2 and y1 > y2:
        sign_x = -1
        sign_y = -1

    val1 = math.fabs(x2 - x1)
    val2 = math.fabs(y2 - y1)

    return [sign_x, sign_y, val1 / val1, val2 / val1]

class GameObject:

    def __init__(self, game, position, velocity, dimensions):
        self.position = position
        self.game = game
        self.velocity = velocity
        self.dimensions = dimensions

    def draw(self):
        pass

    def update(self):
        pass

    def collidesWith(self, other):
        # TODO 5 - Return true if self collides with other, false otherwise
        return abs(self.position[0] - other.position[0]) < abs(self.dimensions[0] + other.dimensions[0]) and \
               abs(self.position[1] - other.position[1]) < abs(self.dimensions[1] + other.dimensions[1])
        pass

class Ball(GameObject):

    def __init__(self, game, position, dimensions):
        velocity = [0, 0]
        super().__init__(game, position, velocity, dimensions)
        self.speed = [0, 0, 0]
        self.clock = 0

    def draw(self):
        # TODO 2.2 - Draw ball as a red circle.
        pygame.draw.circle(self.game.window, RED, self.position, BALL_RADIUS, 0)
        pass

    def update(self):
        # TODO 3.1 - Calculate new position. Cast the velocity to int!
        if self.velocity[0] != 0 and self.velocity[1] != 0:
            if self.speed[2] == 0:
                self.clock = SLOW_TIME
                self.speed[0] = math.fabs(self.velocity[0] / SLOW_TIME)
                self.speed[1] = math.fabs(self.velocity[1] / SLOW_TIME)
                self.speed[2] = 1

            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            self.clock -= 1

            if self.clock == 0:
                self.velocity[0] = 0
                self.velocity[1] = 0

            if self.velocity[0] > 0:
                self.velocity[0] -= self.speed[0]
            elif self.velocity[0] < 0:
                self.velocity[0] += self.speed[0]

            if self.velocity[1] > 0:
                self.velocity[1] -= self.speed[1]
            elif self.velocity[1] < 0:
                self.velocity[1] += self.speed[1] 
        
        # TODO 3.2 - When ball hits up and down walls, bounce the ball off the wall.
        if self.position[1] - self.dimensions[1] < 0:
            self.velocity[1] *= -1

        if self.position[1] + self.dimensions[1] > HEIGHT:
            self.velocity[1] *= -1

        if self.position[0] - self.dimensions[0] < 0:
            self.velocity[0] *= -1

        if self.position[0] + self.dimensions[0] > WIDTH:
            self.velocity[0] *= -1

        if self.position[0] >= HOLE_POSITION[0] and self.position[0] <= HOLE_POSITION[0] + HOLE_RADIUS * 2 - BALL_RADIUS * 2 \
            and self.position[1] >= HOLE_POSITION[1] and self.position[1] <= HOLE_POSITION[1] + HOLE_RADIUS * 2 - BALL_RADIUS * 2:
                self.reset()
                self.game.leftPlayerScore = 0

    def reset(self):
        self.game.ball = Ball(self.game, [200, 600], [BALL_RADIUS, BALL_RADIUS])
        self.game.gameObjects.remove(self)
        self.game.gameObjects.append(self.game.ball)

    def onCollision(self, other):
        pass
        
class Hole(GameObject):

    def __init__(self, game, position, dimensions):
        velocity = [0, 0]
        super().__init__(game, position, velocity, dimensions)

    def draw(self):
        # TODO 2.2 - Draw ball as a red circle.
        pygame.draw.circle(self.game.window, WHITE, self.position, BALL_RADIUS + 5, 0)
        pass

    def update(self):
        pass

    def reset(self):
        pass

    def onCollision(self, other):
        pass

class Wall(GameObject):

    def __init__(self, game, position, dimensions):
        velocity = [0, 0]
        super().__init__(game, position, velocity, dimensions)

    def draw(self):
        # TODO 2.2 - Draw ball as a red circle.
        pygame.draw.rect(self.game.window, BROWN, (self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]))
        pass

    def update(self):
        pass

    def reset(self):
        pass

    def onCollision(self, other):
        pass

class Game:

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (600, 0)
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Pixel Golf')

        # Don't touch this
        self.gameObjects = []
        self.leftPlayerScore = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed_level = 0

        self.ball = Ball(self, [200, 600], [BALL_RADIUS, BALL_RADIUS])
        self.hole = Hole(self, [200, 50], [BALL_RADIUS + 5, BALL_RADIUS + 5])
        self.wall1 = Wall(self, [0, 0], [100, 250])
        self.wall2 = Wall(self, [0, 450], [100, 250])
        self.wall3 = Wall(self, [300, 0], [200, 700])
        self.wall4 = Wall(self, [175, 300], [125, 100])

        self.gameObjects.append(self.ball)
        self.gameObjects.append(self.hole)
        self.gameObjects.append(self.wall1)
        self.gameObjects.append(self.wall2)
        self.gameObjects.append(self.wall3)
        self.gameObjects.append(self.wall4)

    def run(self):
        while True:
            closed = self.input()
            if closed == 0:
                return 0
            self.update()
            self.draw()

    def collisionDetection(self):
        for target in self.gameObjects:
            if self.ball != target and self.hole != target:
                if self.ball.collidesWith(target):
                    self.ball.onCollision(target)
            if self.hole == target:
                if self.ball.collidesWith(target):
                    for obj in self.gameObjects:
                        obj.reset()
                    break

    def update(self):
        self.collisionDetection()
        for gameObject in self.gameObjects:
            gameObject.update()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    (pos_x, pos_y) = pygame.mouse.get_pos()
                    distance = total_distance(pos_x, pos_y, self.ball.position)
                    tang_list = tg(pos_x, pos_y, self.ball.position[0] + BALL_RADIUS, self.ball.position[1] + BALL_RADIUS)

                    self.speed_level = distance / 10
                    if self.speed_level > 10:
                        self.speed_level = 10

                    if self.speed_level == 0:
                        self.speed_level += 1
                    
                    self.velocity_x = tang_list[0] * tang_list[2] * self.speed_level
                    self.velocity_y = tang_list[1] * tang_list[3] * self.speed_level

                if mouse_presses[2]:
                    if self.speed_level > 0:
                        self.leftPlayerScore += 1

                    self.ball.velocity[0] = self.velocity_x
                    self.ball.velocity[1] = self.velocity_y
                    self.velocity_x = 0
                    self.velocity_y = 0
                    self.speed_level = 0

    def draw(self):
        # TODO 2.1 - Fill window with BLACK.
        self.window.fill(DARKG)

        # TODO 2.1 - Draw all objects from self.gameObjects.
        for gameObject in self.gameObjects:
            gameObject.draw()

        myfont1 = pygame.font.SysFont("Comic Sans MS", 30)
        label1 = myfont1.render("High Score : " + str(self.leftPlayerScore), 1, (0,0,0))
        self.window.blit(label1, (20,20))
        
        if self.speed_level > 0:
            myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
            label2 = myfont2.render("Power", 1, (0,0,0))
            self.window.blit(label2, (450,560))
            pygame.draw.rect(self.window, BLACK, (460, 580, 20, 100)) 
            for i in range(0, int(self.speed_level), 1):
                pygame.draw.rect(self.window, (0, 255 - 20 * i, 0), 
                    (460, 670 - 10 * i, 20, 10))

        if self.speed_level >= 4:
            for i in range(3, int(self.speed_level), 1):
                pygame.draw.rect(self.window, (255, 255 - 20 * i, 0), 
                    (460, 670 - 10 * i, 20, 10))

        if self.speed_level >= 10:
            for i in range(9, int(self.speed_level), 1):
                pygame.draw.rect(self.window, RED, 
                    (460, 670 - 10 * i, 20, 10))

        # TODO 2.1 - Update display.
        pygame.display.update()

        # TODO 2.1 - Set frame rate to 60 FPS.
        frame_rate.tick(60)

game = Game()
closed = game.run()
sys.exit()