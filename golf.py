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
LEVELS = 3

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
        return self.position[0] >= HOLE_POSITION[0] and self.position[0] <= HOLE_POSITION[0] + HOLE_RADIUS * 2 - BALL_RADIUS \
            and self.position[1] >= HOLE_POSITION[1] and self.position[1] <= HOLE_POSITION[1] + HOLE_RADIUS * 2 - BALL_RADIUS

class Ball(GameObject):

    def __init__(self, game, position, dimensions):
        velocity = [0, 0]
        super().__init__(game, position, velocity, dimensions)
        self.speed = [0, 0, 0]
        self.clock = 0

    def draw(self):
        pygame.draw.circle(self.game.window, RED, self.position, BALL_RADIUS, 0)
        pass

    def update(self):
        if self.velocity[0] > 300 or \
            self.velocity[1] > 300:
            self.reset()

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
                return

            if self.velocity[0] > 0:
                self.velocity[0] -= self.speed[0]
            elif self.velocity[0] < 0:
                self.velocity[0] += self.speed[0]

            if self.velocity[1] > 0:
                self.velocity[1] -= self.speed[1]
            elif self.velocity[1] < 0:
                self.velocity[1] += self.speed[1] 
        
        if self.position[1] - self.dimensions[1] < 0:
            self.velocity[1] *= -1
            return

        if self.position[1] + self.dimensions[1] > HEIGHT:
            self.velocity[1] *= -1
            return

        if self.position[0] - self.dimensions[0] < 0:
            self.velocity[0] *= -1
            return

        if self.position[0] + self.dimensions[0] > WIDTH:
            self.velocity[0] *= -1
            return                

        for target in self.game.gameObjects:
            if self.game.ball != target and self.game.hole != target:
                if self.velocity[0] > 0 and \
                    self.position[0] + self.dimensions[0] > target.position[0] and \
                    self.position[0] < target.position[0] and \
                    self.position[1] + self.dimensions[1] > target.position[1] and \
                    self.position[1] < target.position[1] + target.dimensions[1]:
                    self.velocity[0] *= -1
                    continue

                if self.velocity[0] < 0 and \
                    self.position[0] < target.position[0] + target.dimensions[0] and \
                    self.position[0] + self.dimensions[0] > target.position[0] + target.dimensions[0] and \
                    self.position[1] + self.dimensions[1] > target.position[1] and \
                    self.position[1] < target.position[1] + target.dimensions[1]:
                    self.velocity[0] *= -1
                    continue

                if self.velocity[1] > 0 and \
                    self.position[1] + self.dimensions[1] > target.position[1] and \
                    self.position[1] < target.position[1] and \
                    self.position[0] + self.dimensions[0] > target.position[0] and \
                    self.position[0] < target.position[0] + target.dimensions[0]:
                    self.velocity[1] *= -1
                    continue

                if self.velocity[1] < 0 and \
                    self.position[1] < target.position[1] + target.dimensions[1] and \
                    self.position[1] + self.dimensions[1] > target.position[1] + target.dimensions[1] and \
                    self.position[0] + self.dimensions[0] > target.position[0] and \
                    self.position[0] < target.position[0] + target.dimensions[0]:
                    self.velocity[1] *= -1
                    continue

    def reset(self):
        self.game.ball = Ball(self.game, [200, 600], [BALL_RADIUS, BALL_RADIUS])
        self.game.gameObjects.remove(self)
        self.game.gameObjects.append(self.game.ball)

    def onCollision(self, other, side):
        if side == 1:
            self.velocity[0] *= -1
            self.velocity[1] *= 1
        
class Hole(GameObject):

    def __init__(self, game, position, dimensions):
        velocity = [0, 0]
        super().__init__(game, position, velocity, dimensions)

    def draw(self):
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

        self.gameObjects = []
        self.leftPlayerScore = 0
        self.highScore = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed_level = 0
        self.signs = [0, 0, 0]

        self.ball = 0
        self.hole = 0

    def lobby(self):
        while True:
            pygame.init()
            bg_img = pygame.image.load('golf.jpg')
            bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
            self.window.blit(bg_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        (pos_x, pos_y) = pygame.mouse.get_pos()
                        if pos_x > 170 and pos_x < 310 and \
                            pos_y > 150 and pos_y < 200:
                            return 1

                        if pos_x > 160 and pos_x < 335 and \
                            pos_y > 225 and pos_y < 275:
                            return 2
            myfont1 = pygame.font.SysFont("Comic Sans MS", 75)
            label1 = myfont1.render("Pixel Golf" , 1, (0,0,0))
            self.window.blit(label1, (120,75))

            pygame.draw.rect(self.window, RED, (170, 150, 140, 50))

            label1 = myfont1.render("Start" , 1, (0,0,0))
            self.window.blit(label1, (180,150))


            pygame.draw.rect(self.window, RED, (160, 225, 175, 50))

            label1 = myfont1.render("Levels" , 1, (0,0,0))
            self.window.blit(label1, (170,225))

            pygame.display.update()
            frame_rate.tick(60)

    def level_lobby(self):
        while True:
            bg_img = pygame.image.load('golf.jpg')
            bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
            self.window.blit(bg_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        (pos_x, pos_y) = pygame.mouse.get_pos()
                        if pos_x > 100 and pos_x < 150 and \
                            pos_y > 150 and pos_y < 200:
                            return 0

                        if pos_x > 200 and pos_x < 250 and \
                            pos_y > 150 and pos_y < 200:
                            return 1

                        if pos_x > 300 and pos_x < 350 and \
                            pos_y > 150 and pos_y < 200:
                            return 2

                        if pos_x > 0 and pos_x < 125 and \
                            pos_y > 650 and pos_y < HEIGHT:
                            return -2                        

            myfont1 = pygame.font.SysFont("Comic Sans MS", 75)
            label1 = myfont1.render("Levels" , 1, (0,0,0))
            self.window.blit(label1, (175,75))

            pygame.draw.rect(self.window, RED, (100, 150, 50, 50))

            label1 = myfont1.render("0" , 1, (0,0,0))
            self.window.blit(label1, (110,150))


            pygame.draw.rect(self.window, RED, (200, 150, 50, 50))

            label1 = myfont1.render("1" , 1, (0,0,0))
            self.window.blit(label1, (210,150))

            pygame.draw.rect(self.window, RED, (300, 150, 50, 50))

            label1 = myfont1.render("2" , 1, (0,0,0))
            self.window.blit(label1, (310, 150))

            pygame.draw.rect(self.window, RED, (0, 650, 125, 50))

            label1 = myfont1.render("Back" , 1, (0,0,0))
            self.window.blit(label1, (0, 650))

            pygame.display.update()
            frame_rate.tick(60)

    def run(self, lvl):
        f = open("level" + str(lvl) + ".txt", "r")

        self.ball = Ball(self, [200, 600], [BALL_RADIUS, BALL_RADIUS])
        self.hole = Hole(self, [200, 50], [BALL_RADIUS + 5, BALL_RADIUS + 5])
        self.gameObjects.append(self.ball)
        self.gameObjects.append(self.hole)

        line = f.readline()
        while line:
            params = line.split()
            if params[0] == "wall":
                wal = Wall(self, [int(params[1]), int(params[2])], [int(params[3]), int(params[4])])
                
                self.gameObjects.append(wal)
            line = f.readline()
        f.close()

        while True:
            closed = self.input()
            if closed == 0:
                return 0
            if self.update():
                return 1
            self.draw()
        return 0

    def collisionDetection(self):
        for target in self.gameObjects:
            if self.hole == target:
                if self.ball.collidesWith(target):
                    for obj in self.gameObjects:
                        obj.reset()
                    if self.highScore == 0 or (self.highScore != 0 and self.highScore > self.leftPlayerScore):
                        self.highScore = self.leftPlayerScore
                    self.leftPlayerScore = 0
                    return 1
        return 0

    def update(self):
        if self.collisionDetection():
            return 1
        for gameObject in self.gameObjects:
            gameObject.update()
        return 0

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == KEYDOWN and event.key == K_q:
                self.ball.reset()
                self.leftPlayerScore = 0

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
                    
                    self.velocity_x = tang_list[0] * tang_list[2] * (self.speed_level / 2)
                    self.velocity_y = tang_list[1] * tang_list[3] * (self.speed_level / 2)

                    self.signs[0] = tang_list[0]
                    self.signs[1] = tang_list[1]
                    self.signs[2] = tang_list[3]

                if mouse_presses[2]:
                    if self.speed_level > 0:
                        self.leftPlayerScore += 1

                    self.ball.velocity[0] = self.velocity_x
                    self.ball.velocity[1] = self.velocity_y
                    self.velocity_x = 0
                    self.velocity_y = 0
                    self.speed_level = 0
                    self.signs = [0, 0, 0]

    def reset(self):
        self.gameObjects = []

    def draw(self):
        self.window.fill(DARKG)

        for gameObject in self.gameObjects:
            gameObject.draw()

        myfont1 = pygame.font.SysFont("Comic Sans MS", 30)
        label1 = myfont1.render("Score : " + str(self.leftPlayerScore), 1, (0,0,0))
        self.window.blit(label1, (20,20))

        if self.highScore > 0:
            label1 = myfont1.render("High Score : " + str(self.highScore), 1, (0,0,0))
            self.window.blit(label1, (20,40))
        
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

        if self.signs[0] != 0:
            pygame.draw.line(self.window, WHITE, (self.ball.position[0], self.ball.position[1]), (self.ball.position[0]+ 20 * self.signs[0], self.ball.position[1] + 20 * self.signs[1]))
            pygame.display.flip()

        pygame.display.update()

        frame_rate.tick(60)

game = Game()
closedLobby = -1
start = 0

while closedLobby < 0:
    closedLobby = game.lobby()
    if closedLobby == 0:
        sys.exit()
        break

    if closedLobby == 1:
        break

    if closedLobby == 2:
        closedLobby = game.level_lobby()
        if closedLobby == -1:
            sys.exit()
            break

        if closedLobby == -2:
            continue

        start = closedLobby

if closedLobby != -1 and closedLobby != 0:
    for i in range(start, LEVELS):
        closed = game.run(i)
        if closed == 0:
            break
        game.reset()
    sys.exit()