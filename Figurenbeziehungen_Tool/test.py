import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((1080, 720))


mode = False
result = ''
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if result != '':
                print(result)
                result = ''
            mode = not mode

        if mode and event.type == pygame.KEYDOWN:
            result += event.unicode
