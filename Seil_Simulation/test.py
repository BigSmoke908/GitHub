'''import sys
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((1920, 1080))

stickIMG = pygame.image.load('stick.png')

i = 0

while True:
    screen.fill((100, 100, 100))
    stickIMG = pygame.transform.rotate(stickIMG, i)
    i = 0
    screen.blit(stickIMG, (100, 100))

    time.sleep(0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            state = pygame.mouse.get_pressed()

            if state[0]:
                i = -1
            elif state[2]:
                i = 1

    pygame.display.update()
'''

zeug = [(18.35895898094998, 99.81)]

print(zeug[0][0])
