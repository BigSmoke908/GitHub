import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((2000, 2000))
maxima = [0, 204]


def mandelbrot(re, im, max_iter):
    global maxima
    c = complex(re, im)
    z = 0.0j

    maxi = []

    for i in range(max_iter):
        z = z ** 2 + c
        neu = z.real ** 2 + z.imag ** 2
        maxi.append(neu)
        if neu >= 4:
            color = i * (255 / max_iter)
            return int((color / 1.8) + 50), int((color / 1.6) + 20), int((color / 1.4)), 0
    return 255, 154, 95, max(maxi)


counter = 0
alles = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, 'mandelbrot.png')
            pygame.quit()
            print(max(alles))
            sys.exit()

    if counter <= 2000:
        for i in range(counter, counter + 50):
            for j in range(2000):
                farbe = mandelbrot((i - 1200) / 500, (j - 1000) / 500, 500)
                alles.append(farbe[3])
                try:
                    pygame.draw.rect(screen, (farbe[0], farbe[1], farbe[2]), (i, j, 1, 1))
                except:
                    print(farbe)
                    sys.exit()
    counter += 50
    pygame.display.update()