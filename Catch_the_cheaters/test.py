import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((2000, 2000))


def mandelbrot(re, im, max_iter):
    c = complex(re, im)
    z = 0.0j

    for i in range(max_iter):
        z = z**2 + c
        if (z.real**2 + z.imag**2) >= 4:
            color = i * (255/max_iter)
            return color, 200, 200
    return 255, 200, 200


def render(bild):
    x = 0
    for h in bild:
        for v in h:
            pygame.draw.rect(screen, v, (bild.index(h), h.index(v), 1, 1))
        x += 1
        if x % 10 == 0:
            print(x//10)
    pygame.display.update()


counter = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if counter <= 2000:
        for i in range(counter, counter + 50):
            for j in range(2000):
                farbe = mandelbrot((i - 1200)/500, (j - 1000)/500, 5)
                pygame.draw.rect(screen, farbe, (i, j, 1, 1))
    pygame.display.update()
    counter += 50

