import pygame
import matplotlib.pyplot as plt
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
Pixel = pygame.image.load('Salesman.png').convert_alpha()
FirstTime = True

def render_route(a, b, FirstTime):
    start = [a[0], a[1]]
    end = [b[0], b[1]]
    if start[0] < end[0]:
        end = [a[0], a[1]]
        start = [b[0], b[1]]

    if FirstTime:
        print(end[1] - start[1] / end[0] - start[0])
        FirstTime = False
    for x in range(start[0], end[0] + 1):
        screen.blit(Pixel, (x, ((end[1]-start[1]/end[0]-start[0])*(x-start[0]))//1))
    return FirstTime


def render_weg(a, b):
    start, end, = a, b
    if a[0] > b[0]:
        end, start = a, b

    m = (end[0]-start[0]) / (end[1]+start[1])
    n = start[1] - (m*start[0])
    for x in range(start[0], end[0]):
        screen.blit(Pixel, (x, m*x+n))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    #FirstTime = render_route([100, 100], [1000, 1000], FirstTime)
    render_weg([10, 10],[30,30])

    pygame.display.update()