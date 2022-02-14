import random
import sys
import time

import pygame
import math

pygame.init()

FK = (3840, 2160)
FHD = (1920, 1080)
UHD = (2560, 1440)
HD = (1080, 720)

screen = pygame.display.set_mode(HD)



i = 0
x = 100
y = 100
while True:
    if i % 1000 == 0:
        y += 1


    pygame.draw.circle(screen, (100, 100, 100), (x, y), 20)

    pygame.display.update()
