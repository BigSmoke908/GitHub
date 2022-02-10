import sys
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((1920, 1080))

stickIMG = pygame.image.load('stick.png')

while True:
    screen.fill((100, 100, 100))

    screen.blit(stickIMG, (100, 100))

    time.sleep(0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    stickIMG = pygame.transform.rotate(stickIMG, 1)