import sys
import pygame


pygame.init()
screen = pygame.display.set_mode((1920, 1080))


def get_value(x, steps=0):
    if len(str(x)) == 1:
        return steps
    alles = [int(i) for i in str(x)]

    j = 1
    for i in alles:
        j *= i
    return get_value(j, steps + 1)


def get_color(x, y):
    res = get_value(x * y)
    return [res * 36.428 for n in range(3)]


def render(bild):
    for i in bild:
        for j in i:
            pygame.draw.rect(screen, j, (bild.index(i), i.index(i), 1, 1))
    pygame.display.update()


Set = [[get_color(i, j) for i in range(1920)] for j in range(1080)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    render(Set)
