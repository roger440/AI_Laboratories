# -*- coding: utf-8 -*-
from constants import *
from pygame.locals import *
import pygame, time
from service import *

class GUI():

    def initPyGame(self, dimension):
        # init the pygame
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(WHITE)
        return screen


    def closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
         # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()


    def movingDrone(self, currentMap, path, speed=1, markSeen=True):
        # animation of a drone on a path
        time.sleep(1)
        screen = self.initPyGame((currentMap.n * 20, currentMap.m * 20))

        drona = pygame.image.load("drona.png")

        for i in range(len(path)):
            screen.blit(self.image(currentMap), (0, 0))

            if markSeen:
                brick = pygame.Surface((20, 20))
                brick.fill(GREEN)
                for j in range(i + 1):
                    for var in DIRECTIONS:
                        x = path[j][0]
                        y = path[j][1]

                        screen.blit(brick, (y * 20, x * 20))

            screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
            pygame.display.flip()
            time.sleep(0.5* speed)
        time.sleep(30)
        self.closePyGame()


    def image(self, currentMap, colour=BLUE, background=WHITE):
        # creates the image of a map

        imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if (currentMap.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def mapImage(self, currentMap):
        screen = self.initPyGame((currentMap.n * 20, currentMap.m * 20))
        screen.blit(self.image(currentMap),(0,0))
        pygame.display.flip()
        self.closePyGame()

